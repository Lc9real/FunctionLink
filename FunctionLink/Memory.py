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
                        output += f'\nKeys: {fileKeys}\nContent: {open(f"./Memory/{self.memory_key}/Key/{file}").read()}\n\n'
                        break
            return output

        def add_Memory_Sytem(self, path: str):
            pass

        def get_Memory_Sytem(self):
            pass


        def clear_Memory(self):
            os.remove(f"./Memory/{self.memory_key}")
            os.makedirs(f"./Memory/{self.memory_key}")
            os.makedirs(f"./Memory/{self.memory_key}/Key/")
            os.makedirs(f"./Memory/{self.memory_key}/System/")









