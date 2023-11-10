import asyncio

from llama_cpp import Llama

class LinkContainer():
    def __init__(self, name: str, description: str, func: callable, coroutine: bool=False):
        self.Name = name
        self.Description = description
        self.func = func
        self.coroutine = coroutine

class Link():
    def __init__(self, llm: Llama, tools: list[LinkContainer]):
        self.llm = llm
        self.tools = tools
    def __call__(self, prompt: str, tempreture: float=0, stop: list[str]=["\n\n", ";"], stream: bool=False) -> dict[str: str]:
        def generate(prompt: str, tempreture, stop, stream: bool) -> dict[str: str]:
            allDic = {"Full": "", "Response": "", "Reason": ""}
            inputToken = self.llm.tokenize(prompt.encode('utf-8'))
            commandConditions = [False, False, False]
            outputToken = []
            Commandfunc = None
            inputForFunc = ""
            funcName = ""
            responseNcommand = ""
            iscoroutine = False
            for token in self.llm.generate(inputToken, top_k=40, top_p=0.95, temp=tempreture, repeat_penalty=1.1, reset=True):
                outputToken.append(token)
                if len(outputToken) >= 2:
                    if (outputToken[-2] == 8257 and outputToken[-1] == 1903) or (outputToken[-2] == 2 and outputToken[-1] == 28799):
                        outputToken = outputToken[:-2]
                        text = self.llm.detokenize(outputToken).decode("utf-8")
                        allDic["Reason"] = "Nyet"
                        return allDic
                currentTokenstr: str = self.llm.detokenize([token]).decode("utf-8")
                if stream:
                    print(currentTokenstr, end='')
                text = self.llm.detokenize(outputToken).decode("utf-8")
                if commandConditions[0]:
                    if commandConditions[1]:
                        if commandConditions[2]:
                            if ")" in currentTokenstr:
                                if iscoroutine:
                                    Output = asyncio.run(Commandfunc(inputForFunc))
                                else:
                                    Output = Commandfunc(inputForFunc)
                                input_ = self.llm.detokenize(outputToken).decode("utf-8") + " Output: '" + Output + "'"
                                prom = prompt + input_
                                gen = generate(prom, tempreture, stop, stream)
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
                                iscoroutine = element.coroutine
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

        generated = generate(prompt, tempreture, stop, stream)
        if stream:
            print("")
        return generated