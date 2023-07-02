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

        # Build the regular expression pattern
        self.pattern = r'({})|\b([a-zA-Z_][a-zA-Z0-9_]*)\b|([0-9]+)|"([^"\\]*(?:\\.[^"\\]*)*)"|([^\w\s])'.format(
            '|'.join(map(re.escape, self.keywords + self.punctuators))
        )

    def tokenize_c_program(self, c_program):
        tokens = []
        # Remove comments by replacing them with whitespace
        c_program = re.sub(r'(\/\*[\s\S]*?\*\/|\/\/.*)', lambda m: ' ' * len(m.group()), c_program)
        for match in re.finditer(self.pattern, c_program):
            keyword, identifier, constant, string_literal, punctuator = match.groups()
            if keyword:
                tokens.append({'Type': 'KEYWORD', 'Value': keyword})
            elif identifier:
                tokens.append({'Type': 'IDENTIFIER', 'Value': identifier})
            elif constant:
                tokens.append({'Type': 'CONSTANT', 'Value': constant})
            elif string_literal:
                tokens.append({'Type': 'STRING_LITERAL', 'Value': string_literal})
            elif punctuator:
                tokens.append({'Type': 'PUNCTUATOR', 'Value': punctuator})
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
