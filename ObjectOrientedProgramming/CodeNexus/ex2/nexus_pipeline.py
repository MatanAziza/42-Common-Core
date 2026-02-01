#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Union, Dict, List, Protocol
from colorama import Fore


class InputStage:
    def process(self, data: Any) -> Any:
        print(Fore.GREEN + f"Input: {data}" + Fore.WHITE)
        if isinstance(data, Dict):
            data["adapter"] = "JSON"
            return data
        elif isinstance(data, str):
            all_elements = data.split(",")
            new_dict = {key: 0 for key in all_elements}
            for key in all_elements:
                old_value: int = new_dict.get(key)
                new_dict.update({key: old_value + 1})
            new_dict["adapter"] = "CSV"
            return new_dict
        elif isinstance(data, list):
            list_list = [elem.split(":") for elem in data]
            dict_1 = {key: [] for key, _ in list_list}
            for key, _ in dict_1.items():
                key_list = []
                for key2, value2 in list_list:
                    if key2 == key:
                        key_list.append(value2)
                dict_1.update({key: key_list})
            dict_1["adapter"] = "Stream"
            return dict_1
        else:
            return {}


class TransformStage:
    def process(self, data: Any) -> Any:
        if data.get("adapter", "error") == "JSON":
            print("Transform: ", end='')
            try:
                data.pop("adapter")
                value = float(data.get("value"))
                unit = data.get("unit")
                if value < 20:
                    range_value = "Cold"
                elif value < 30:
                    range_value = "Normal"
                else:
                    range_value = "Hot"
                sensor = data.get("sensor")
                matchups = ["temp", "press", "humid"]
                if sensor in matchups:
                    print("Enriched with metadata and validation")
                    return {
                        "sensor": sensor,
                        "value": value,
                        "range": range_value,
                        "unit": unit,
                        "adapter": "JSON",
                    }
                else:
                    raise ValueError(
                        "Wrong sensor provided.Please be careful with data"
                    )
            except ValueError as e:
                print(f"{type(e).__name__}: {e}\n")
                return {}
        elif data.get("adapter", "error") == "Stream":
            print("Transform: ", end='')
            try:
                avg = []
                readings = 0
                units = []
                data.pop("adapter")
                matchups = ["temp", "press", "humid"]
                for key, value in data.items():
                    if key in matchups:
                        values_list = data.get(key)
                        values_list = [float(elem) for elem in values_list]
                        sum_nb = sum(values_list) / len(values_list)
                        current_avg = round(sum_nb, 1)
                        avg.append(current_avg)
                        readings += len(values_list)
                        units.append(key)
                print("Aggregated and filtered")
                if data.get("chaining", "error") == 1:
                    list_dict = []
                    unit_match = {"temp": "C", "press": "hPa", "humid": "g/m3"}
                    for i in range(len(units)):
                        list_dict.append({
                            "sensor": units[i],
                            "value": avg[i],
                            "unit": unit_match.get(units[i])
                        })
                    return list_dict
                else:
                    return {
                        "readings": readings,
                        "avg": avg,
                        "units": units,
                        "adapter": "Stream",
                    }
            except ValueError as e:
                print(f"{type(e).__name__}: {e}\n")
                return {}
        elif data.get("adapter", "error") == "CSV":
            print("Transform: ", end='')
            data.pop("adapter")
            nb_actions = data.get("action", "error")
            user_log = data.get("login", "error")
            if user_log != "error":
                print("Parsed and structured data")
                return {"action": nb_actions, "adapter": "CSV"}
            else:
                return {"user": "NotLogged", "adapter": "CSV"}
        else:
            return {}


class OutputStage:
    def process(self, data: Any) -> Any:
        if data.get("adapter", "error") == "JSON":
            try:
                matchups = {
                    "temp": "temperature",
                    "press": "pressure",
                    "humid": "humidity",
                }
                sensor = matchups.get(data.get("sensor"))
                unit = data.get("unit")
                value = data.get("value")
                range_value = data.get("range")
                if sensor == "temperature" and unit != "C" and unit != "F":
                    raise ValueError("Wrong Unit for data measured.")
                elif sensor == "pressure" and unit != "hPa":
                    raise ValueError("Wrong Unit for data measured.")
                elif sensor == "humidity" and unit != "g/m3":
                    raise ValueError("Wrong Unit for data measured.")
                else:
                    str_ret = f"Processed {sensor} reading: {value} "
                    str_ret += f"{unit} ({range_value} range)"
                    return f"Output: {str_ret}\n"
            except ValueError as e:
                print(f"{type(e).__name__}: {e}\n")
                return
        elif data.get("adapter", "error") == "Stream":
            str_ret = f"Output: Stream summary: {data.get('readings')}"
            str_ret += " readings, "
            values, units = data.get("avg"), data.get("units")
            for i in range(len(values)):
                str_ret += f"avg n°{i + 1}: {values[i]}"
                if units[i] == "temp":
                    str_ret += "°C, "
                elif units[i] == "press":
                    str_ret += " hPa, "
                elif units[i] == "humid":
                    str_ret += " g/m3, "
            str_ret = str_ret[: str_ret.rindex(",")]
            return str_ret + "\n"
        else:
            if data.get("adapter", "error") == "CSV":
                return "Output: User not logged, no actions possible\n"
            else:
                actions = data.get("action")
                str_ret = f"Output: User activity logged: {actions} "
                return str_ret + "actions processed\n"


class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        pass


class ProcessingPipeline(ABC):
    stages: List[ProcessingStage] = []

    @classmethod
    def add_stage(cls: Any, stage: ProcessingStage) -> None:
        i_stage = "Input validation and parsing"
        t_stage = "Data transformation and enrichment"
        o_stage = "Output formatting and delivery"
        if type(stage).__name__ == "InputStage":
            print(f"Stage {len(cls.stages) + 1}: {i_stage}")
        elif type(stage).__name__ == "TransformStage":
            print(f"Stage {len(cls.stages) + 1}: {t_stage}")
        if type(stage).__name__ == "OutputStage":
            print(f"Stage {len(cls.stages) + 1}: {o_stage}")
        cls.stages.append(stage)

    @classmethod
    def clear_stages(cls: Any):
        for _ in range(len(cls.stages)):
            cls.stages.pop(0)

    @classmethod
    def get_stages(cls: Any) -> List[ProcessingStage]:
        return cls.stages

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass


class JSONAdapter(ProcessingPipeline):
    stages: List[ProcessingStage] = []

    def __init__(self, pipeline_id: str) -> None:
        self.id = pipeline_id

    def process(self, data: Any) -> Union[str, Any]:
        stages = JSONAdapter.get_stages()
        for stage in stages:
            data = stage.process(data)
            if not data:
                return
        return data


class CSVAdapter(ProcessingPipeline):
    stages: List[ProcessingStage] = []

    def __init__(self, pipeline_id: str) -> None:
        self.id = pipeline_id

    def process(self, data: Any) -> Union[str, Any]:
        stages = CSVAdapter.get_stages()
        for stage in stages:
            data = stage.process(data)
            if not data:
                return
        return data


class StreamAdapter(ProcessingPipeline):
    stages: List[ProcessingStage] = []

    def __init__(self, pipeline_id: str) -> None:
        self.id = pipeline_id

    def process(self, data: Any) -> Union[str, Any]:
        stages = StreamAdapter.get_stages()
        stages_name = [type(stage).__name__ for stage in stages]
        for stage in stages:
            if "OutputStage" not in stages_name and isinstance(data, Dict):
                data["chaining"] = 1
            data = stage.process(data)
            if not data:
                return
        return data


class NexusManager:
    pipelines: List[ProcessingPipeline] = []

    @classmethod
    def add_pipeline(cls: Any, pipeline: ProcessingPipeline) -> None:
        cls.pipelines.append(pipeline)

    @classmethod
    def get_pipeline(cls: Any) -> List[ProcessingPipeline]:
        return cls.pipelines

    @staticmethod
    def process_data(pipeline: ProcessingPipeline, data: Any) -> None:
        return pipeline.process(data)


if __name__ == "__main__":
    print(Fore.YELLOW + "=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===")
    print(Fore.WHITE + "\nInitialysing Nexus Manager...\n")
    JSONAdapter.add_stage(InputStage())
    JSONAdapter.add_stage(TransformStage())
    JSONAdapter.add_stage(OutputStage())
    print()
    CSVAdapter.add_stage(InputStage())
    CSVAdapter.add_stage(TransformStage())
    CSVAdapter.add_stage(OutputStage())
    print()
    StreamAdapter.add_stage(InputStage())
    StreamAdapter.add_stage(TransformStage())
    StreamAdapter.add_stage(OutputStage())
    print()
    print(Fore.YELLOW + "=== Multi-Format Data Processing ===\n" + Fore.WHITE)
    NexusManager.add_pipeline(JSONAdapter("JSON_001"))
    NexusManager.add_pipeline(StreamAdapter("STREAM_001"))
    NexusManager.add_pipeline(CSVAdapter("CSV_001"))
    pipelines = NexusManager.get_pipeline()
    datas = [
        {"sensor": "press", "value": 22.5, "unit": "hPa"},
        ["temp:22", "temp:26", "press:1013", "temp:21.8", "press:55"],
        "login,action,action,timestamp",
    ]
    same = ""
    for i in range(len(pipelines)):
        type_pipe = str(type(pipelines[i]).__name__)
        print(
            f"Processing {type_pipe[: type_pipe.index('Adapter')]}"
            f" data through {same}pipeline..."
        )
        print(NexusManager.process_data(pipelines[i], datas[i]))
        same = "same "
    for i in range(len(pipelines)):
        pipelines[i].clear_stages()
    print(Fore.YELLOW + "=== Pipeline Chaining Demo ===" + Fore.WHITE)
    print("Pipeline A -> Pipeline B\n")
    stream = StreamAdapter("STREAM_002")
    stream.add_stage(InputStage())
    stream.add_stage(TransformStage())
    print()
    data = NexusManager.process_data(stream, [
        "temp:22",
        "temp:26",
        "press:1013",
        "temp:21.8",
        "press:55"
    ])
    json = JSONAdapter("JSON_002")
    json.add_stage(InputStage())
    json.add_stage(TransformStage())
    json.add_stage(OutputStage())
    print()
    for elem in data:
        print(NexusManager.process_data(json, elem))
    print(Fore.YELLOW + "=== Error Recovery Test ===" + Fore.WHITE)
    print("Simulating pipeline failure...")
    NexusManager.process_data(
                            pipelines[0],
                            {"sensor": "presss", "value": 22.5, "unit": "hPa"}
                              )
    print("Nexus Integration complete. All systems operational.")
