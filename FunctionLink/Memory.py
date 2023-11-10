import os


class Memory_System():
        def __init__(self, MemoryKey:str):
            self.memory_key = MemoryKey
            if not os.path.exists(f"./Memory/{self.memory_key}"):
                os.makedirs(f"./Memory/{self.memory_key}")
            if not os.path.exists(f"./Memory/{self.memory_key}/Key/"):
                os.makedirs(f"./Memory/{self.memory_key}/Key/")
            if not os.path.exists(f"./Memory/{self.memory_key}/System/"):
                os.makedirs(f"./Memory/{self.memory_key}/System/")
            if not os.path.exists(f"./Memory/{self.memory_key}/{self.memory_key}.memory"):
                open(f"./Memory/{self.memory_key}/{self.memory_key}.memory", "w").close()

        def add_Memory_Keys(self, keys: list[str], content: str):
            name = ""
            for key in keys:
                name += key + ", "
            name = name[:-2]
            file = open(f"./Memory/{self.memory_key}/Key/{name}.memory", "w")
            file.write(content)

        def get_Memory_Keys(self, content:str):
            files = os.listdir(f"./Memory/{self.memory_key}/Key/")
            output:str = ""
            for file in files:
                fileKeys = file[:-7]
                keys = fileKeys.split(", ")
                for key in keys:
                    if key.lower() in content.lower():
                        f = open(f"./Memory/{self.memory_key}/Key/{file}")
                        output += f'\nKeys: {fileKeys}\nContent: {f.read()}\n\n'
                        f.close()
                        break
            return output

        def add_Memory_Sytem(self, path: str, name: str, content: str):
            if not os.path.exists(f"./Memory/{self.memory_key}/System/{path}/"):
                os.makedirs(f"./Memory/{self.memory_key}/System/{path}/")
            f = open(f"./Memory/{self.memory_key}/System/{path}/{name}.memory", "w")
            f.write(content)
            f.close()

        def get_Memory_Sytem(self, path: str, filename: str=""):
            if filename:
                return f"{path}{filename}:\n" + open(f"./Memory/{self.memory_key}/System/{path}/{filename}.memory", "r").read()
            dir = os.walk(f"./Memory/{self.memory_key}/System/{path}")
            nextdir = next(dir)
            tempDir = {"Folders": nextdir[1], "Files": nextdir[2]}

            return tempDir

        def add_Memory_shortTerm(self, content: str):
            f = open(f"./Memory/{self.memory_key}/{self.memory_key}.memory", "a")
            f.write(content + "\n")
            f.close()

        def get_Memory_shortTerm(self):
            f = open(f"./Memory/{self.memory_key}/{self.memory_key}.memory", "r")
            return f.read()

        def add_summary(self, content: str):
            f = open(f"./Memory/{self.memory_key}/{self.memory_key}.memory", "w")
            f.write(content + "\n")
            f.close()

        def clear_Memory(self):
            os.remove(f"./Memory/{self.memory_key}")
            os.makedirs(f"./Memory/{self.memory_key}")
            os.makedirs(f"./Memory/{self.memory_key}/Key/")
            os.makedirs(f"./Memory/{self.memory_key}/System/")
