
# fájl mentése
def uploaded_file(file, filePath):

    with open(filePath, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

