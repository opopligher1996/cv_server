from thumbnails import get_thumbnail

file_name = get_thumbnail('test_pic.jpeg', '50x30', crop='center')
print(file_name)
