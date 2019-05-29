from antigate import AntiGate

API_KEY = "401446c86f02e43141a7333030229c4d"


def get_code(file_name: str) -> str:
    return str(AntiGate(API_KEY, file_name))
