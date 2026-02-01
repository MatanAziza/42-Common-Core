#!/usr/bin/env python3

from typing import Any, List
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """Abstract method for data processing"""
    @abstractmethod
    def process(self, data: Any) -> str:
        """process data"""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """checks if a data is valid for a certain type"""
        pass

    def format_output(self, result: str) -> str:
        """return a certain output"""
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """numeric processor"""
    def process(self, data: List[Any]) -> str:
        """process numeric values"""
        if self.validate(data) is True:
            print("Validation: Numeric data verified")
            new_data = [int(nbr) for nbr in data]
            nb_nbr = len(new_data)
            summ = sum(new_data)
            avg = summ/nb_nbr
            return f"Processed {nb_nbr} numeric values, sum={summ}, avg={avg}"
        else:
            print("Validation: Data not valid")
            return ""

    def validate(self, data: Any) -> bool:
        """checks if the data is all ints"""
        try:
            new_data: List[int] = []
            for elem in data:
                new_data.append(int(elem))
            if len(new_data) == 0:
                return False
            return True
        except ValueError:
            return False


class TextProcessor(DataProcessor):
    """text processor"""
    def process(self, data: str) -> str:
        if self.validate(data) is True:
            print("Validation: Log data verified")
            length = len(data)
            nb_words = len(data.split(" "))
            return f"Processed text: {length} characters, {nb_words} words"
        else:
            print("Validation: Data not valid")
            return ""

    def validate(self, data: Any) -> bool:
        try:
            data += ""
            return True
        except TypeError:
            return False


class LogProcessor(DataProcessor):
    def process(self, data: str) -> str:
        if self.validate(data) is True:
            print("Validation: Log data verified")
            if "INFO" in data:
                return f"[INFO] {data[:4]} level detected: {data[6:]}"
            else:
                return f"[ALERT] {data[:5]} level detected: {data[7:]}"
        else:
            print("Validation: Data not valid")
            return ""

    def validate(self, data: Any) -> bool:
        if "INFO" not in data and "ERROR" not in data:
            return False
        else:
            return True


def process_data(processor: DataProcessor, data: Any) -> Any:
    print(f"Processing data: '{data}' with {type(processor).__name__}")
    return processor.process(data)


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    data = ["1", "2", "3", "4", "5"]
    print("Initializing Numeric Processor...")
    numeric_processor = NumericProcessor()
    result = process_data(numeric_processor, data)
    print(numeric_processor.format_output(result)) if result != "" else 0

    data = "Hello Nexus World"
    print("\nInitializing Text Processor...")
    text_processor = TextProcessor()
    result = process_data(text_processor, data)
    print(text_processor.format_output(result)) if result != "" else 0

    data = "ERROR: Connection timeout"
    print("\nInitializing Log Processor...")
    log_processor = LogProcessor()
    result = process_data(log_processor, data)
    print(log_processor.format_output(result)) if result != "" else 0

    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    processors = [numeric_processor, text_processor, log_processor]
    datas = [["1", "2", "3"], 5, "INF: System ready"]
    for i in range(3):
        result = process_data(processors[i], datas[i])
        print(f"Result 1: {result}") if result != "" else 0
    print("\nFoundation systems online. Nexus ready for advanced streams.")
