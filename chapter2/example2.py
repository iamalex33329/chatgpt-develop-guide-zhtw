import tiktoken

encoder = tiktoken.encoding_for_model('gpt-3.5-turbo')
print('encoder of gpt-3.5-turbo: ' + encoder.name)

encoder = tiktoken.encoding_for_model('gpt-4')
print('encoder of gpt-4: ' + encoder.name)

tokens = encoder.encode('how are you')
print('tokens: ' + str(tokens))
print('length of token: ' + str(len(tokens)))
print('decode tokens: ' + encoder.decode(tokens))
