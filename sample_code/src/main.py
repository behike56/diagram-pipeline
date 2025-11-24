from inbound.stdin_adapter import StdinInputAdapter
from outbound.file_adapter import FileIOAdapter
from core.usecase import ProcessUseCase


def main():
    stdin_adapter = StdinInputAdapter()
    file_io = FileIOAdapter("data/input.txt", "data/output.txt")

    usecase = ProcessUseCase(stdin_adapter, file_io)
    result = usecase.execute()

    print("==== result ====")
    print(result)


if __name__ == "__main__":
    main()
