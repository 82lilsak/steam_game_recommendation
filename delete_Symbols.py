title = 'Marvel’sSpider - Man: MilesMorales'
print(title)
no_save = ['/', ':', '-', '*', '@', '#', '$', '%', '^', '&', '(', ')', '{', '}', '[', ']', '<', '>', '?', '\\', '"',
           "'", '=', '|', ',', '.', '`', '~', '+', '’']

for i in range(len(no_save)):
    title = title.replace(no_save[i], ' ')
print(title)

print(len(title))
print(len(no_save))
