%{
# include <cerrno>
# include <climits>
# include <cstdlib>
# include <cstring> // strerror
# include <string>

# include "vexpparser/scanner.h"
# include "vexpparser/interpreter.h"
# include "vexp_parser.hh"
# include "location.hh"

# define YY_NO_UNISTD_H

// Original yyterminate() macro returns int. Since we're using Bison 3 variants
// as tokens, we must redefine it to change type from `int` to `Parser::semantic_type`
# define yyterminate() Vexp::Parser::make_END(Vexp::location());

# define YY_USER_ACTION  m_driver.increaseLocation (yyleng);

%}

%option noyywrap nodefault
%option c++
%option yyclass="Scanner"
%option prefix="Vexp_"

/* Single character tokens */

NEWLINE             "\n"|"\r\n"
BLANK               [ \t\r]

AT                  "@"
COMMA               ","
HASH                "#"
DELAY               "##"
DOT                 "."
EQ                  "="
STORE1              ":<"
STORE2              ">:"
COLON               ":"
IDX_PRT_SEL_PLUS    "+:"
IDX_PRT_SEL_MINUS   "-:"
SEMICOLON           ";"
OPEN_BRACKET        "\("
CLOSE_BRACKET       "\)"
OPEN_SQ_BRACKET     "\["
CLOSE_SQ_BRACKET    "\]"
OPEN_SQ_BRACE       "{"
CLOSE_SQ_BRACE      "}"


/* Tokens related to numbers */

EXP                 "e"|"E"
UNDERSCORE          "_"
SIGN                {PLUS}|{MINUS}
X                   "x"|"X"
Z                   "z"|"Z"

DIGIT_DECIMAL       [0-9]
DIGIT_DECMIAL_NZ    [1-9]
DIGIT_BINARY        [0-1]|{X}|{Z}
DIGIT_OCTAL         [0-7]|{X}|{Z}
DIGIT_HEX           [0-9a-fA-F]|{X}|{Z}

BASE_DECIMAL        '[sS]?[dD]
BASE_BINARY         '[sS]?[bB]
BASE_OCTAL          '[sS]?[oO]
BASE_HEX            '[sS]?[hH]

NUM_REAL_EXP        {NUM_UNSIGNED}({DOT}{NUM_UNSIGNED})?{EXP}({SIGN})?{NUM_UNSIGNED}

BIN_VALUE           {DIGIT_BINARY}({UNDERSCORE}|{DIGIT_BINARY})*
OCT_VALUE           {DIGIT_OCTAL}({UNDERSCORE}|{DIGIT_OCTAL})*
HEX_VALUE           {DIGIT_HEX}({UNDERSCORE}|{DIGIT_HEX})*

%x in_hex_val
%x in_oct_val
%x in_bin_val
%s in_number

NUM_REAL            {NUM_UNSIGNED}{DOT}{NUM_UNSIGNED}|{NUM_REAL_EXP}
NUM_UNSIGNED        {DIGIT_DECIMAL}({UNDERSCORE}|{DIGIT_DECIMAL})*

/* Identifiers */

DOLLAR              \$
SYSTEM_ID           \$[a-zA-Z0-9_\$]+
SIMPLE_ID           [a-zA-Z_][a-zA-Z0-9_$]*
ESCAPED_ID          \\{SIMPLE_ID}
MACRO_IDENTIFIER    `{SIMPLE_ID}

MACRO_TEXT          .*\n

%x in_define
%x in_define_t

/* Attributes */

ATTRIBUTE_START     \(\*
ATTRIBUTE_END       \*\)

/* Comments */
COMMENT_LINE        "//".*\n

COMMENT_BEGIN       "/*"
COMMENT_END         "*/"

%x in_comment

/* Strings : this is not a good definition */
/* you should have used state rather than RE */

STRING              \".*\"

/* Operators */

STAR                "\*"
PLUS                "+"
MINUS               "-"
ASL                 "<<<"
ASR                 ">>>"
LSL                 "<<"
LSR                 ">>"
DIV                 "/"
POW                 "**"
MOD                 "%"
GTE                 ">="
LTE                 "<="
GT                  ">"
LT                  "<"
L_NEG               "!"
L_AND               "&&"
L_OR                "||"
C_EQ                "==="
L_EQ                "=="
C_NEQ               "!=="
L_NEQ               "!="
B_NEG               "~"
B_AND               "&"
B_OR                "|"
B_XOR               "^"
B_EQU               "^~"|"~^"
B_NAND              "~&"
B_NOR               "~|"
TERNARY             "?"
IMPLY               "|->"
IMPLY_NEXT          "|=>"

%%


{ATTRIBUTE_START}      { return Vexp::Parser::make_ATTRIBUTE_START(Vexp::location());}
{ATTRIBUTE_END}        { return Vexp::Parser::make_ATTRIBUTE_END(Vexp::location()); }

{COMMENT_LINE}         { /* IGNORE */ }
{COMMENT_BEGIN}        {BEGIN(in_comment);                    ;}

<in_comment>.|\n       { /* IGNORE */ }
<in_comment>{COMMENT_END} {BEGIN(INITIAL);                     }


{AT}                   { return Vexp::Parser::make_AT               ( verilog_expr::voperator::AT, Vexp::location()       ) ; /*this should be an operator*/ }
{COMMA}                { return Vexp::Parser::make_COMMA            ( Vexp::location()                      ) ;}
{DELAY}                { return Vexp::Parser::make_DELAY            ( Vexp::location()                      ) ;}
{HASH}                 { return Vexp::Parser::make_HASH             ( Vexp::location()                      ) ;}
{DOT}                  { return Vexp::Parser::make_DOT              ( Vexp::location()                      ) ;}
{STORE1}               { return Vexp::Parser::make_STORE1           ( Vexp::location()                      ) ;}
{STORE2}               { return Vexp::Parser::make_STORE2           ( Vexp::location()                      ) ;}
{COLON}                { return Vexp::Parser::make_COLON            ( Vexp::location()                      ) ;}
{IDX_PRT_SEL_PLUS}     { return Vexp::Parser::make_IDX_PRT_SEL_PLUS ( Vexp::location()                      ) ;}
{IDX_PRT_SEL_MINUS}    { return Vexp::Parser::make_IDX_PRT_SEL_MINUS( Vexp::location()                      ) ;}
{SEMICOLON}            { return Vexp::Parser::make_SEMICOLON        ( Vexp::location()                      ) ;}
{OPEN_BRACKET}         { return Vexp::Parser::make_OPEN_BRACKET     ( Vexp::location()                      ) ;}
{CLOSE_BRACKET}        { return Vexp::Parser::make_CLOSE_BRACKET    ( Vexp::location()                      ) ;}
{OPEN_SQ_BRACKET}      { return Vexp::Parser::make_OPEN_SQ_BRACKET  ( Vexp::location()                      ) ;}
{CLOSE_SQ_BRACKET}     { return Vexp::Parser::make_CLOSE_SQ_BRACKET ( Vexp::location()                      ) ;}
{OPEN_SQ_BRACE}        { return Vexp::Parser::make_OPEN_SQ_BRACE    ( Vexp::location()                      ) ;}
{CLOSE_SQ_BRACE}       { return Vexp::Parser::make_CLOSE_SQ_BRACE   ( Vexp::location()                      ) ;}
{STAR}                 { return Vexp::Parser::make_STAR             ( verilog_expr::voperator::STAR    , Vexp::location() ) ;}
{PLUS}                 { return Vexp::Parser::make_PLUS             ( verilog_expr::voperator::PLUS    , Vexp::location() ) ;}
{MINUS}                { return Vexp::Parser::make_MINUS            ( verilog_expr::voperator::MINUS   , Vexp::location() ) ;}
{ASL}                  { return Vexp::Parser::make_ASL              ( verilog_expr::voperator::ASL     , Vexp::location() ) ;}
{ASR}                  { return Vexp::Parser::make_ASR              ( verilog_expr::voperator::ASR     , Vexp::location() ) ;}
{LSL}                  { return Vexp::Parser::make_LSL              ( verilog_expr::voperator::LSL     , Vexp::location() ) ;}
{LSR}                  { return Vexp::Parser::make_LSR              ( verilog_expr::voperator::LSR     , Vexp::location() ) ;}
{DIV}                  { return Vexp::Parser::make_DIV              ( verilog_expr::voperator::DIV     , Vexp::location() ) ;}
{POW}                  { return Vexp::Parser::make_POW              ( verilog_expr::voperator::POW     , Vexp::location() ) ;}
{MOD}                  { return Vexp::Parser::make_MOD              ( verilog_expr::voperator::MOD     , Vexp::location() ) ;}
{GTE}                  { return Vexp::Parser::make_GTE              ( verilog_expr::voperator::GTE     , Vexp::location() ) ;}
{LTE}                  { return Vexp::Parser::make_LTE              ( verilog_expr::voperator::LTE     , Vexp::location() ) ;}
{GT}                   { return Vexp::Parser::make_GT               ( verilog_expr::voperator::GT      , Vexp::location() ) ;}
{LT}                   { return Vexp::Parser::make_LT               ( verilog_expr::voperator::LT      , Vexp::location() ) ;}
{L_NEG}                { return Vexp::Parser::make_L_NEG            ( verilog_expr::voperator::L_NEG   , Vexp::location() ) ;}
{L_AND}                { return Vexp::Parser::make_L_AND            ( verilog_expr::voperator::L_AND   , Vexp::location() ) ;}
{L_OR}                 { return Vexp::Parser::make_L_OR             ( verilog_expr::voperator::L_OR    , Vexp::location() ) ;}
{C_EQ}                 { return Vexp::Parser::make_C_EQ             ( verilog_expr::voperator::C_EQ    , Vexp::location() ) ;}
{L_EQ}                 { return Vexp::Parser::make_L_EQ             ( verilog_expr::voperator::L_EQ    , Vexp::location() ) ;}
{C_NEQ}                { return Vexp::Parser::make_C_NEQ            ( verilog_expr::voperator::C_NEQ   , Vexp::location() ) ;}
{L_NEQ}                { return Vexp::Parser::make_L_NEQ            ( verilog_expr::voperator::L_NEQ   , Vexp::location() ) ;}
{B_NEG}                { return Vexp::Parser::make_B_NEG            ( verilog_expr::voperator::B_NEG   , Vexp::location() ) ;}
{B_AND}                { return Vexp::Parser::make_B_AND            ( verilog_expr::voperator::B_AND   , Vexp::location() ) ;}
{B_OR}                 { return Vexp::Parser::make_B_OR             ( verilog_expr::voperator::B_OR    , Vexp::location() ) ;}
{B_XOR}                { return Vexp::Parser::make_B_XOR            ( verilog_expr::voperator::B_XOR   , Vexp::location() ) ;}
{B_EQU}                { return Vexp::Parser::make_B_EQU            ( verilog_expr::voperator::B_EQU   , Vexp::location() ) ;}
{B_NAND}               { return Vexp::Parser::make_B_NAND           ( verilog_expr::voperator::B_NAND  , Vexp::location() ) ;}
{B_NOR}                { return Vexp::Parser::make_B_NOR            ( verilog_expr::voperator::B_NOR   , Vexp::location() ) ;}
{TERNARY}              { return Vexp::Parser::make_TERNARY          ( verilog_expr::voperator::TERNARY , Vexp::location() ) ;}
{IMPLY}                { return Vexp::Parser::make_IMPLY            ( Vexp::location()                      ) ; }
{IMPLY_NEXT}           { return Vexp::Parser::make_IMPLY_NEXT       ( Vexp::location()                      ) ; }
{EQ}                   { return Vexp::Parser::make_EQ               ( Vexp::location()                      ) ; /*this is just a symbol not OP*/ }

{BASE_DECIMAL}         {return Vexp::Parser::make_DEC_BASE(Vexp::location());}
{BASE_HEX}             {BEGIN(in_hex_val); return Vexp::Parser::make_HEX_BASE(Vexp::location());}
{BASE_OCTAL}           {BEGIN(in_oct_val); return Vexp::Parser::make_OCT_BASE(Vexp::location());}
{BASE_BINARY}          {BEGIN(in_bin_val); return Vexp::Parser::make_BIN_BASE(Vexp::location());}

<in_bin_val>{BIN_VALUE} {BEGIN(INITIAL); return Vexp::Parser::make_BIN_VALUE(yytext,Vexp::location()); }
<in_oct_val>{OCT_VALUE} {BEGIN(INITIAL); return Vexp::Parser::make_OCT_VALUE(yytext,Vexp::location()); }
<in_hex_val>{HEX_VALUE} {BEGIN(INITIAL); return Vexp::Parser::make_HEX_VALUE(yytext,Vexp::location()); }

{NUM_REAL}             { return Vexp::Parser::make_NUM_REAL(yytext, Vexp::location()); }
{NUM_UNSIGNED}         { return Vexp::Parser::make_UNSIGNED_NUMBER(yytext, Vexp::location()); }

{MACRO_IDENTIFIER}     {
    return Vexp::Parser::make_MACRO_IDENTIFIER(yytext, Vexp::location());
}

{ESCAPED_ID}           {
    return Vexp::Parser::make_ESCAPED_ID(yytext, Vexp::location());
}
{SIMPLE_ID}|{SYSTEM_ID} {        
    if(!strcmp(yytext, "$forall"))
        return Vexp::Parser::make_FORALL(Vexp::location());
    if(!strcmp(yytext, "$exist"))
        return Vexp::Parser::make_EXIST(Vexp::location());
    return Vexp::Parser::make_SIMPLE_ID(yytext, Vexp::location());
}

{DOLLAR} {
  return Vexp::Parser::make_DOLLAR(Vexp::location());
}

{STRING}               { return Vexp::Parser::make_STRING(yytext, Vexp::location());}

<*>{BLANK}+          { /*loc.step ();*/ }
<*>{NEWLINE}+        { /*loc.lines (yyleng); loc.step ();*/ /*note: you can count linebreak here*/ }

<<EOF>>                { return yyterminate();}
.                      {
    std::cout << "[VexpParser] : Unknown character ["<< yytext <<"]" << std::endl;
}

%%