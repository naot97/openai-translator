GPT35_INPUT_PRICING  = 0.0015
GPT35_OUTPUT_PRICING = 0.002
LIMIT_TOKEN_NUMBER   = 1500
prompt               =  \
'''I want you to act as a Translator. I will speak to you in any language and you will translate it to {}. Please follow 3 next rules. Firstly, please do not remove the characters "||", it is a very important symbol. Secondly, Never add more any punctuation. Thirdy, I want you to only reply the translation, do not write explanations. My paragraph is {}'''
max_attemp = 3