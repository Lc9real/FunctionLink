from llama_cpp import Llama

class LinkContainer():
    def __init__(self, Name: str, Description: str, func: callable,):
        self.Name = Name
        self.Description = Description
        self.func = func

class Link():
    def __init__(self, llm: Llama, tools: list[LinkContainer]):
        self.llm = llm
        self.tools = tools
    def __call__(self, prompt: str, tempreture=0, stop: list[str]=["\n\n", ";"],) -> dict[str: str]:
        def generate(prompt: str, tempreture, stop) -> dict[str: str]:
            allDic = {"Full": "", "Response": "", "Reason": ""}
            inputToken = self.llm.tokenize(prompt.encode('utf-8'))
            commandConditions = [False, False, False]
            outputToken = []
            Commandfunc = None
            inputForFunc = ""
            funcName = ""
            responseNcommand = ""
            for token in self.llm.generate(inputToken, top_k=40, top_p=0.95, temp=tempreture, repeat_penalty=1.1, reset=True):
                outputToken.append(token)
                if len(outputToken) >= 2:
                    if (outputToken[-2] == 8257 and outputToken[-1] == 1903) or (outputToken[-2] == 2 and outputToken[-1] == 28799):
                        outputToken = outputToken[:-2]
                        text = self.llm.detokenize(outputToken).decode("utf-8")
                        allDic["Reason"] = "Nyet"
                        return allDic
                currentTokenstr: str = self.llm.detokenize([token]).decode("utf-8")
                text = self.llm.detokenize(outputToken).decode("utf-8")
                if commandConditions[0]:
                    if commandConditions[1]:
                        if commandConditions[2]:
                            if ")" in currentTokenstr:
                                Output = Commandfunc(inputForFunc)
                                input_ = self.llm.detokenize(outputToken).decode("utf-8") + " Output: '" + Output + "'"
                                prom = prompt + input_
                                gen = generate(prom, tempreture, stop)
                                allDic["Reason"] = gen["Reason"]
                                allDic["Response"] = responseNcommand + gen["Response"]
                                allDic["Full"] = input_ + gen["Full"]
                                return allDic
                            else:
                                inputForFunc += currentTokenstr
                        elif "(" in currentTokenstr:
                            commandConditions[2] = True
                    else:
                        funcName += currentTokenstr
                        for element in self.tools:
                            if element.Name in funcName:
                                Commandfunc = element.func
                                commandConditions[1] = True
                                break
                elif "/" in currentTokenstr:
                    responseNcommand += " "
                    commandConditions[0] = True
                for stopResons in stop:
                    if stopResons in text:
                        allDic["Reason"] = stopResons
                        allDic["Full"] = allDic["Full"]
                        return allDic
                if not commandConditions[0]:
                    responseNcommand += currentTokenstr
                allDic["Full"] += currentTokenstr
                allDic["Response"] = responseNcommand
            return allDic
        return generate(prompt, tempreture, stop)