from langchain import PromptTemplate

CoT = PromptTemplate(
    input_variables=["rahmen_code", "prompt", "sample"],
    template="""create java code function for this problem: {prompt}.
    Here are some examples: {sample}.
    Use this class as the framework:{rahmen_code}\nAdd the function into this frame and gibt me the class Solution back\n
    """
)

# Tree of Thought Prompting
ToT = PromptTemplate(
    input_variables=["rahmen_code", "prompt", "sample"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}.
    Here are some examples: {sample}.
    Use this class as the framework:{rahmen_code}\n

    Consider multiple possible solutions, evaluate their effectiveness, and explain the reasoning behind choosing the 
    final solution."""
)

# Few-Shot Prompting
Few_shot = PromptTemplate(
    input_variables=["rahmen_code", "prompt", "sample"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}.
    Here are some examples: {sample}.
    Use this class as the framework:{rahmen_code}\n

    Use the examples as a guide to create a similar solution tailored to this problem.
    """
)

# Zero-Shot Prompting
Zero_shot = PromptTemplate(
    input_variables=["rahmen_code", "prompt"],
    template="""you are helpful programmer, create java code function for this problem: {prompt}.
    Here are some examples: {sample}.\n
    """
)
