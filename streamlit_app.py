import re
import streamlit as st
import pandas as pd

class CTokenizer:
    def __init__(self):
        # Define keywords and punctuators
        self.keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int',
            'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile',
            'while'
        ]
        self.punctuators = [
            '{', '}', '[', ']', '(', ')', '.', '->', '++', '--', '&', '*', '+', '-',
            '~', '!', '/', '%', '<<', '>>', '<', '>', '<=', '>=', '==', '!=', '^',
            '|', '&&', '||', '?', ':', ';', '...', '=', '*=', '/=', '%=', '+=', '-=',
            '<<=', '>>=', '&=', '^=', '|=', ','
        ]

        # Build the regular expression patterns
        self.keyword_pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, self.keywords)))
        self.identifier_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        self.constant_pattern = r'\b([0-9]+)\b'
        self.string_literal_pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"'
        self.punctuator_pattern = r'({})'.format('|'.join(map(re.escape, self.punctuators)))

    def tokenize_c_program(self, c_program):
        tokens = []
        # Remove comments by replacing them with whitespace
        c_program = re.sub(r'(\/\*[\s\S]*?\*\/|\/\/.*)', lambda m: ' ' * len(m.group()), c_program)
        
        # Tokenize the program
        patterns = [
            (self.keyword_pattern, 'KEYWORD'),
            (self.identifier_pattern, 'IDENTIFIER'),
            (self.constant_pattern, 'CONSTANT'),
            (self.string_literal_pattern, 'STRING_LITERAL'),
            (self.punctuator_pattern, 'PUNCTUATOR')
        ]
        
        for pattern, token_type in patterns:
            for match in re.finditer(pattern, c_program):
                tokens.append({'Type': token_type, 'Value': match.group()})
                
        return tokens


def main():
    st.title("C Tokenizer")
    uploaded_file = st.file_uploader("Upload a .c file", type=["c"])

    if uploaded_file is not None:
        c_program = uploaded_file.read().decode("utf-8")
        tokenizer = CTokenizer()
        tokens = tokenizer.tokenize_c_program(c_program)
        st.header("Tokens")
        df = pd.DataFrame(tokens)
        st.dataframe(df)
        if st.button("Export Tokens"):
            export_data = df.to_string(index=False)
            export_filename = "c_tokens.txt"
            st.download_button(
                label="Download Tokens",
                data=export_data,
                file_name=export_filename,
                mime="text/plain"
            )


if __name__ == '__main__':
    main()
