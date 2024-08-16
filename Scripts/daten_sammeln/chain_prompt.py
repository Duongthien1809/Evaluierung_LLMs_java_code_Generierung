from langchain import PromptTemplate

CoT = PromptTemplate(
    input_variables=["rahmen_code", "prompt", "sample"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}.Use this class as 
    the framework:{rahmen_code}\nAdd the function into this frame and gibt me the class Solution back.\nHere are some 
    examples: {sample}. Please think step by step.\nNotice: Don't forget to add import if it needed!"""

)

# Tree of Thought Prompting
ToT = PromptTemplate(
    input_variables=["rahmen_code", "prompt", "sample"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}.
    Use this class as the framework:{rahmen_code}\n
    Here are some examples: {sample}.\n
    Consider multiple possible solutions, evaluate their effectiveness, and explain the reasoning behind choosing the 
    final solution.\nNotice: Don't forget to add import if it needed!"""
)

# Few-Shot Prompting
Few_shot = PromptTemplate(
    input_variables=["rahmen_code", "prompt", "sample"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}.
    Use this class as the framework:{rahmen_code}\n
    Here are some examples: {sample}.\n
    Use the examples as a guide to create a similar solution tailored to this problem.\nNotice: Don't forget to add import if it needed!
    """
)

# Zero-Shot Prompting
Zero_shot = PromptTemplate(
    input_variables=["rahmen_code", "prompt"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}. Use this class as 
    the framework:{rahmen_code}\nAdd the function into this frame and gibt me the class Solution back.\nNotice: Don't 
    forget to add import if it needed!"""
)
