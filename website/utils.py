
#doesn't work now due to % sign, decodeURI?
def url_tag(path, pk):
    path =  '{% url \'' + path + '\' ' + pk +  ' %}'
    return '"{}"'.format(path)



#given /Users/Principe/Desktop/cs50w/final/final/media/uploads/vehicle_pictures
#/Screen_Shot_2021-07-12_at_7.53.12_PM.png
#give only media level and down
def image_path(path):
    list = path.split('/')
    path = list[-4:]
    return '/'.join(path)


def number_extractor(string):
    # list = []
    # for i in str(string):
    #     if i.isnumeric():
    #         list.append(i)
    #     ''.join(list)
    result = ''.join(i for i in str(string) if i.isnumeric())
    return int(result)