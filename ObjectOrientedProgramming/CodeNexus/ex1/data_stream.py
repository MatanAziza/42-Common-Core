#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List, Union


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    @abstractmethod
    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)
        self.stats = {}

    def process_batch(self, data_batch: List[Any]) -> str:
        self.data = data_batch
        length_data = len(data_batch)
        temp: str = ""
        for elem in data_batch:
            if "temp" in elem:
                temp += elem[5:]
                break
        if temp != "":
            self.readings = length_data
            self.avg_temp = temp
            return f"{length_data} readings processed, avg temp: {temp}°C"
        else:
            return "No temperature was present in the datas given"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria == "high":
            return [e for e in data_batch if float(e[e.index(":")+1:]) >= 20]
        elif criteria == "medium":
            return [e for e in data_batch if float(e[e.index(":")+1:]) >= 25]
        elif criteria == "low":
            return [e for e in data_batch if float(e[e.index(":")+1:]) >= 30]
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        new_list = [elem.split(":") for elem in self.data]
        return {key: value for key, value in new_list}


class TransactionStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        self.data = data_batch
        length_data = len(data_batch)
        net_flow = 0
        for elem in data_batch:
            if "buy" in elem:
                net_flow += int(elem[4:])
            else:
                net_flow -= int(elem[5:])
        str_ret = f"{length_data} operations, net_flow: "
        if net_flow >= 0:
            str_ret += "+"
        return str_ret + f"{net_flow} units"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria == "high":
            return [e for e in data_batch if int(e[e.index(":")+1:]) >= 150]
        elif criteria == "medium":
            return [e for e in data_batch if int(e[e.index(":")+1:]) >= 100]
        elif criteria == "low":
            return [e for e in data_batch if int(e[e.index(":")+1:]) >= 50]
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        new_list = [elem.split(":") for elem in self.data]
        buys = sum([int(value) for key, value in new_list if key == "buy"])
        sells = sum([int(value) for key, value in new_list if key == "sell"])
        return {"buy": buys, "sells": sells}


class EventStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)

    def process_batch(self, data_batch: List[Any]) -> str:
        self.data: List[str] = data_batch
        length_data = len(data_batch)
        nb_errors = 0
        for elem in data_batch:
            if "error" in elem:
                nb_errors += 1
        str_ret = f"{length_data} events, {nb_errors} error"
        if nb_errors > 1:
            str_ret += "s"
        return str_ret + " detected"

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria == "high":
            return [elem for elem in data_batch if elem == "error"]
        elif criteria == "medium":
            return [e for e in data_batch if int(e[e.index(":")+1:]) >= 100]
        elif criteria == "low":
            return [e for e in data_batch if int(e[e.index(":")+1:]) >= 50]
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        types = {key: 0 for key in self.data}
        for elem in self.data:
            old_value: int = types.get(elem)
            types.update({elem: old_value + 1})
        return types


class StreamProcessor:
    @staticmethod
    def process_data(datastream: DataStream, data_batch: List[str]) -> str:
        return datastream.process_batch(data_batch)


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print("\nInitializing Sensor Stream...")
    sensor_stream = SensorStream("SENSOR_001")
    sensor_data = ["temp:22.5", "humidity:65", "pressure:1013"]
    StreamProcessor.process_data(sensor_stream, sensor_data)
    print(f"Stream ID: {sensor_stream.stream_id}, Type: Environmental Data")
    print(f"Processing sensor batch: [{", ".join(sensor_data)}]")
    print(f"Sensor analysis: {sensor_stream.process_batch(sensor_data)}")
    print("\nInitializing Transaction Stream...")
    transaction_stream = TransactionStream("TRANS_001")
    data_batch = ["buy:100", "sell:150", "buy:75"]
    print(f"Stream ID: {transaction_stream.stream_id}, Type: Financial Data")
    print(f"Processing transaction batch: {data_batch}")
    print(
        "Transaction analysis: "
        f"{transaction_stream.process_batch(data_batch)}"
        )
    print("\nInitializing Event Stream...")
    event_stream = EventStream("EVENT_001")
    data_batch = ["login", "error", "disconnect"]
    print(f"Stream ID: {event_stream.stream_id}, Type: System Events")
    print(f"Processing event batch: {data_batch}")
    print(f"Event analysis: {event_stream.process_batch(data_batch)}")
    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...\n")
    streams: List[DataStream] = [
                                SensorStream("SENSOR_001"),
                                TransactionStream("TRANS_001"),
                                EventStream("EVENT_001")
                            ]
    datas: List[List[Any]] = [
                    ["temp:22.5", "humidity:65"],
                    ["buy:100", "sell:150", "buy:75", "sell:50"],
                    ["login", "disconnect", "logout"]
                ]
    print("Batch 1 Results:")
    for i in range(len(streams)):
        result = "- "
        if isinstance(streams[i], SensorStream):
            result += "Sensor data: "
        if isinstance(streams[i], TransactionStream):
            result += "Transaction data: "
        if isinstance(streams[i], EventStream):
            result += "Event data: "
        result += StreamProcessor.process_data(streams[i], datas[i])
        result = result[:result.index(",")]
        if "processed" not in result:
            result += " processed"
        print(result)

    filter = "high"
    print(f"\nStream filtering active: {filter}-priority data only")
    result = ""
    for i in range(len(streams)):
        new_data = streams[i].filter_data(datas[i], "high")
        result += StreamProcessor.process_data(
            streams[i],
            new_data
            )
        result = result[:result.rindex(",")]
        if isinstance(streams[i], SensorStream):
            result = result[:result.index("readings processed")]
        if isinstance(streams[i], TransactionStream):
            result = result[:result.index("operations")]
        if isinstance(streams[i], EventStream):
            result = result[:result.index("event")]
    sensor, trans, event = result.strip().split(" ")
    result = "Filtered results: "
    if float(sensor) > 0:
        result += f"{sensor} critical sensor alerts, "
    if float(trans) > 0:
        result += f"{trans} large transactions, "
    if float(event) > 0:
        result += f"{event} important events"
    print(result)
    print("\nAll streams processed successfully. Nexus troughput optimal.")
