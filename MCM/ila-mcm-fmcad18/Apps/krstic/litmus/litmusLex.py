
import ply.lex as lex
tokens = (
    'ALTERNATIVE',
    'W',
    'R',
    'F',
    'FLAG',
    'ID',
    'RELATION',
    'RL',
    'FORBIDDEN',
    'PERMITTED',
    'REQ',
    'LC',
    'RC',
    'VA',
    'PA',
    'DATA',
    'TO',
    'EQ'
    )

t_ALTERNATIVE = r'[Aa]lternative'
t_W  = r'[Ww]rite'
t_R  = r'[Rr]ead'
t_F  = r'[Ff]ence'
t_FLAG  = r'(RMW)|(Acquie)|(Release)|(MFENCE)'

def t_ID(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

t_RELATION = r'Relationship'
t_RL = r'(rf)|(fr)|(po)|(co)'
t_FORBIDDEN = r'Forbidden'
t_PERMITTED = r'Permitted'
t_REQ = r'[Rr]equired'
t_LC = r'\('
t_RC = r'\)'
t_VA = r'[Vv][Aa]'
t_PA = r'[Pp][Aa]'
t_DATA = r'[Dd][Aa][Tt][Aa]'
t_TO = r'\-\>'
t_EQ = r'='

t_ignore  = ' \t\n'
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex()