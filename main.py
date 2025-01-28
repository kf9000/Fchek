import os
import pickle
import csv
from itertools import zip_longest
from fileWrapper import File_Wrapper
from pathlib import Path
from tools import get_region
from tools import calculate_hash
from tools import printProgressBar
from tools import calculate_file_amount



path = input("Give directory path: ")

suffix_list = [".nds", ".gba", ".z64", ".a26", ".ciso", ".gb", ".gbc", ".nes", ".iso", ".sfc", ".cue", ".wbfs", "smc", "swc", "n64", "v64", ".ogg", ".mp3", ".flac", ".wav", ".mp4", ".png"]
file_list = []
total_files = calculate_file_amount(os.path.join(path, "Games"))/2

index = 0
for subdir, dirs, files in os.walk(os.path.join(path, "Games")):
    for file in files:
        if Path(file).suffix in suffix_list:
            hash: str = calculate_hash(os.path.join(Path(subdir), file))
            suffix = Path(file).suffix
            region = get_region(file)
            file = file.removesuffix(suffix)
            edited_file = file.split("(")
            edited_file = edited_file[0].split("[")
            file = edited_file[0]
            if not file.endswith(" "):
                file = file + " "
            file = file + region
            file = file.replace("_", " ")

            if suffix == ".cue":
                if str(os.path.basename(Path(subdir).parent.absolute())).lower() != "music":
                    file_list.append(File_Wrapper(file, Path(subdir).parent.absolute(), hash))
            else:
                file_list.append(File_Wrapper(file, subdir, hash))
            index += 1
        printProgressBar(index, total_files, prefix="Progress:", suffix="Complete", length=50)

print("Available modes: 1 - export list to file, 2 - import a list and compare, 3 - Create a .txt file listing your files")
mode = input("Choose mode: ")
if mode == "1":
    with open("list.fchek", "wb") as fp:
        pickle.dump(file_list, fp)
        print("File created or edited")

elif mode == "2":
    with open("list.fchek", "rb") as fp:
        quest_list = pickle.load(fp)
        print("Loaded list succesfully")
    
    similar_name_list = []
    quest_different_name_list = []
    local_different_name_list = []

    similar_dir_list = []
    quest_different_dir_list = []
    local_different_dir_list = []

    similar_hash_list = []
    quest_different_hash_list = []
    local_different_hash_list = []

    for local in file_list:
        for quest in quest_list:
            if quest.get_file_name() == local.get_file_name() and quest.get_similar() == False and local.get_similar() == False:
                similar_name_list.append(quest.get_file_name())
                similar_dir_list.append(os.path.basename(quest.get_dir()))
                similar_hash_list.append(quest.get_hash())
                quest.set_similar()
                local.set_similar()
    
    for local in file_list:
        if local.get_similar() == False:
            local_different_name_list.append(local.get_file_name())
            local_different_dir_list.append(os.path.basename(local.get_dir()))
            local_different_hash_list.append(local.get_hash())
    for quest in quest_list:
        if quest.get_similar() == False:
            quest_different_name_list.append(quest.get_file_name())
            quest_different_dir_list.append(os.path.basename(quest.get_dir()))
            quest_different_hash_list.append(quest.get_hash())

    print("\nFiles found locally and in given list: \n")
    index = 0
    for name in similar_name_list:
        print(name, "-", similar_dir_list[index], " - ", similar_hash_list[index])
        index += 1

    index = 0
    print("\nFiles found only locally: \n")
    for name in local_different_name_list:
        print(name, "-", local_different_dir_list[index], " - ", local_different_hash_list[index])
        index += 1

    index = 0
    print("\nFiles found only in given list: \n")
    for name in quest_different_name_list:
        print(name, "-", quest_different_dir_list[index], " - ", quest_different_hash_list[index])
        index += 1

    csv_list = [similar_hash_list, similar_name_list, similar_dir_list, local_different_hash_list, local_different_name_list, local_different_dir_list, quest_different_hash_list, quest_different_name_list, quest_different_dir_list]
    export_data = zip_longest(*csv_list, fillvalue = '')

    export_confirm = input("Convert data to scv? (y/N): ")
    if export_confirm == 'y':
        with open('files.csv', 'w', encoding="utf-8-sig", newline='') as csv_file:
            wr = csv.writer(csv_file)
            wr.writerow(("Equal Hashes","Equal Files", "Equal Folders", "Local Hashes", "Local Files", "Local Folders", "Exported Hashes", "Exported Files", "Exported Folders"))
            wr.writerows(export_data)
        csv_file.close()
        print("Data exported succesfully")

elif mode == "3":        
    text_file = open("file_list.txt", "w", encoding="utf-8-sig")
    parent = ""
    index = 0
    for data in file_list:
        if data.get_dir() != parent:
            parent = data.get_dir()
            text_file.write("[ " + os.path.basename(data.get_dir()) + " ]\n")

        text_file.write("   " + '{:>8}'.format(data.get_hash()) + " | " + data.get_file_name() + "\n")
        index += 1

    text_file.close()
    print("List created succesfully")
else:
    print("Invalid input, shutting down")