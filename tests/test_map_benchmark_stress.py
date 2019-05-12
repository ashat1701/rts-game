from src.Server.Map import Map


def create_map(width, height, rooms, min_room_lenght, max_room_length, random_connections):
    Map(width=width, height=height, max_rooms=rooms, min_room_len=min_room_lenght,
        max_room_len=max_room_length, random_connections=random_connections)


def test_map_benchmark_load(benchmark):
    benchmark(create_map, 200, 200, 5, 5, 5, 4)
