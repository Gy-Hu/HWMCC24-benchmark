%require "3.0"
%skeleton "lalr1.cc" /* -*- C++ -*- */
%verbose
%locations
%defines
%define parser_class_name {Parser}
%define api.value.type variant
%define api.token.constructor
%define api.namespace {Vexp}
%define parse.error verbose
%define parse.trace
%define api.token.prefix {TOK_}

%code requires
{
  #include <vexpparser/vexp.h>
  typedef verilog_expr::VExprAst::VExprAstPtr VExprAstPtr;
  
  namespace Vexp {
    class Scanner;
    class Interpreter;
  };
}

%code top
{
  #include "vexpparser/scanner.h"
  #include "vexp_parser.hh"
  #include "vexpparser/interpreter.h"
  #include "location.hh"

    // yylex() arguments are defined in parser.y
    static Vexp::Parser::symbol_type yylex(Vexp::Scanner &scanner, Vexp::Interpreter &driver) {
        return scanner.get_next_token();
    }
    
    // you can accomplish the same thing by inlining the code using preprocessor
    // x and y are same as in above static function
    // #define yylex(x, y) scanner.get_next_token()
    
    using namespace Vexp;

}

%lex-param { Vexp::Scanner &scanner }
%lex-param { Vexp::Interpreter &driver }
%parse-param { Vexp::Scanner &scanner }
%parse-param { Vexp::Interpreter &driver }


/* Operators Precedence */

%token END 0 "end of file"
%token SEMICOLON "semicolon";

%token <verilog_expr::voperator> STAR
%token <verilog_expr::voperator> PLUS
%token <verilog_expr::voperator> MINUS
%token <verilog_expr::voperator> ASL     
%token <verilog_expr::voperator> ASR     
%token <verilog_expr::voperator> LSL     
%token <verilog_expr::voperator> LSR     
%token <verilog_expr::voperator> DIV     
%token <verilog_expr::voperator> POW     
%token <verilog_expr::voperator> MOD     
%token <verilog_expr::voperator> GTE     
%token <verilog_expr::voperator> LTE     
%token <verilog_expr::voperator> GT      
%token <verilog_expr::voperator> LT      
%token <verilog_expr::voperator> L_NEG   
%token <verilog_expr::voperator> L_AND   
%token <verilog_expr::voperator> L_OR    
%token <verilog_expr::voperator> C_EQ    
%token <verilog_expr::voperator> L_EQ    
%token <verilog_expr::voperator> C_NEQ   
%token <verilog_expr::voperator> L_NEQ   
%token <verilog_expr::voperator> B_NEG   
%token <verilog_expr::voperator> B_AND   
%token <verilog_expr::voperator> B_OR    
%token <verilog_expr::voperator> B_XOR   
%token <verilog_expr::voperator> B_EQU   
%token <verilog_expr::voperator> B_NAND  
%token <verilog_expr::voperator> B_NOR   
%token <verilog_expr::voperator> TERNARY 
%token <verilog_expr::voperator> AT 

%token OPEN_SQ_BRACKET
%token CLOSE_SQ_BRACKET
%token OPEN_BRACKET
%token CLOSE_BRACKET
%token HASH
%token OPEN_SQ_BRACE
%token CLOSE_SQ_BRACE
%token COMMA
%token COLON
%token BIN_BASE 
%token HEX_BASE 
%token OCT_BASE
%token DEC_BASE 
%token IDX_PRT_SEL_PLUS
%token IDX_PRT_SEL_MINUS
%token ATTRIBUTE_START
%token ATTRIBUTE_END
%token EQ
%token DOT
%token DELAY
%token IMPLY
%token IMPLY_NEXT
%token DOLLAR

%token <std::string> SIMPLE_ID
%token <std::string> ESCAPED_ID
%token <std::string> MACRO_IDENTIFIER
%token <std::string> NUM_REAL
%token <std::string> BIN_VALUE
%token <std::string> HEX_VALUE
%token <std::string> OCT_VALUE
%token <std::string> UNSIGNED_NUMBER
%token <std::string> STRING


%nterm<verilog_expr::VExprAst::VExprAstPtr> astroot expression delay_expression next_sequence primary conditional_expression number function_call
%nterm<verilog_expr::VExprAst::VExprAstPtr> concatenation multiple_concatenation
%nterm<verilog_expr::voperator> unary_operator
%nterm<verilog_expr::Attribute> attribute_instances list_of_attribute_instances attr_specs
%nterm<std::string> unsigned_number
%nterm<std::string> hierarchical_identifier_special_name text_macro_usage
%nterm<std::string> identifier simple_identifier escaped_identifier attr_name
%nterm<std::string> string
%nterm<std::string> hierarchical_identifier
%nterm<verilog_expr::VExprAst::VExprAstPtrVec> expressions
%nterm<verilog_expr::SuffixOp>  sq_bracket_expression

/* Operator Precedence */

%right  IMPLY IMPLY_NEXT
%precedence  COLON                 /* Lowest Precedence. */
%right  TERNARY
%left   L_OR
%left   L_AND
%left   B_OR B_NOR
%left   B_EQU B_XOR
%left   B_NAND B_AND
%left   L_EQ C_EQ L_NEQ C_NEQ
%left   GT LT GTE LTE
%left   LSL LSR ASR ASL
%left   PLUS MINUS
%left   STAR DIV MOD
%left   POW
%nonassoc AT                    /* Runtime error */
%left DELAY                 /* Runtime error */

/* turn out the followings are not necessary */
/* %left   OPEN_BRACKET */
/* %left   OPEN_SQ_BRACKET */
%right  L_NEG B_NEG            /* Highest Precedence. */


%%

astroot : expression {
    // TODO : set ast_root
    driver.SetAstRoot($1);
  } 
;

expression :
  primary {
    $$ = $1;
  }
| unary_operator attribute_instances primary{
    $$ = verilog_expr::VExprAst::MakeUnaryAst( $1, $3 );
  }
| delay_expression {
    $$ = $1;
  }
| expression AT  attribute_instances expression{
    // this is the A@B shortcut
    // expression maybe a number or an expression
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::AT, $1, $4);
  }
| expression PLUS  attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::PLUS, $1, $4);
  }
| expression MINUS attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::MINUS, $1, $4);
  }
| expression STAR  attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::STAR, $1, $4);
  }
| expression DIV   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::DIV, $1, $4);
  }
| expression MOD   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::MOD, $1, $4);
  }
| expression L_EQ  attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::L_EQ, $1, $4);
  }
| expression L_NEQ attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::L_NEQ, $1, $4);
  }
| expression C_EQ  attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::C_EQ, $1, $4);
  }
| expression C_NEQ attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::C_NEQ, $1, $4);
  }
| expression L_AND attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::L_AND, $1, $4);
  }
| expression L_OR  attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::L_OR, $1, $4);
  }
| expression POW   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::POW, $1, $4);
  }
| expression LT    attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::LT, $1, $4);
  }
| expression LTE   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::LTE, $1, $4);
  }
| expression GT    attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::GT, $1, $4);
  }
| expression GTE   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::GTE, $1, $4);
  }
| expression B_AND attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::B_AND, $1, $4);
  }
| expression B_OR  attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::B_OR, $1, $4);
  }
| expression B_XOR attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::B_XOR, $1, $4);
  }
| expression B_NOR attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::B_NOR, $1, $4);
  }

| expression IMPLY attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::L_OR, 
      verilog_expr::VExprAst::MakeUnaryAst( verilog_expr::voperator::L_NEG , $1),
      $4); /* !($1) || ($4) */
  }

| expression IMPLY_NEXT attribute_instances expression{
    std::vector<int> tmp;
    tmp.push_back(1);
    $$ = 
      verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::L_OR, 
        verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
          verilog_expr::VExprAst::MakeUnaryAst( verilog_expr::voperator::L_NEG ,$1),
        tmp, {} ), 
      $4); /* (!$1 ## 1) || ($4) */
  }

| expression B_NAND attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::B_NAND, $1, $4);
  }
| expression B_EQU attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::B_EQU, $1, $4);
  }
| expression LSR   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::LSR, $1, $4);
  }
| expression LSL   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::LSL, $1, $4);
  }
| expression ASR   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::ASR, $1, $4);
  }
| expression ASL   attribute_instances expression{
    $$ = verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::ASL, $1, $4);
  }
| conditional_expression {$$=$1;}

| function_call {
      $$ = $1;
  }

;

delay_expression :
  expression DELAY UNSIGNED_NUMBER  {
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($3));
    $$ = verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
      $1,
      tmp, {""} );
  }
| expression DELAY simple_identifier DOT UNSIGNED_NUMBER {
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($5));
    std::vector<std::string> stmp;
    stmp.push_back($3);
    $$ = verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
      $1,
      tmp, stmp );

  }
| expression DELAY OPEN_SQ_BRACKET UNSIGNED_NUMBER COLON UNSIGNED_NUMBER CLOSE_SQ_BRACKET {
  /*1          2        3                4          5      6               7          */
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($4));
    tmp.push_back(verilog_expr::width_to_int($6));
    $$ = verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
      $1,
      tmp, {"", ""} );
  }
| expression DELAY OPEN_SQ_BRACKET simple_identifier DOT UNSIGNED_NUMBER COLON UNSIGNED_NUMBER CLOSE_SQ_BRACKET {
    /*1        2       3              4               5    6                7      8              9*/
    /* e ## [clk.N:M] */
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($6));
    tmp.push_back(verilog_expr::width_to_int($8));
    std::vector<std::string> stmp;
    stmp.push_back($4);
    stmp.push_back("");
    $$ = verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
      $1,
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET UNSIGNED_NUMBER COLON simple_identifier DOT UNSIGNED_NUMBER CLOSE_SQ_BRACKET {
  /* 1         2      3               4              5      6              777       8           9 */
  /* e ## [N:clk.M] */
  std::vector<int> tmp;
  tmp.push_back(verilog_expr::width_to_int($4));
  tmp.push_back(verilog_expr::width_to_int($8));
  std::vector<std::string> stmp;
  stmp.push_back("");
  stmp.push_back($6);
    $$ = verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
      $1,
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET simple_identifier DOT UNSIGNED_NUMBER COLON simple_identifier DOT UNSIGNED_NUMBER CLOSE_SQ_BRACKET {
  /*11111111 22222 333333333333333 44444444444444444 555 666666666666666 77777 88888888888888888 999 aaaaaaaaaaaaaaa bbbbbbbbbbbbbbbb*/
  /* e ## [clk1.N : clk2.M] */
  std::vector<int> tmp;
  tmp.push_back(verilog_expr::width_to_int($6));
  tmp.push_back(verilog_expr::width_to_int($10));
  std::vector<std::string> stmp;
  stmp.push_back($4);
  stmp.push_back($8);
    $$ = verilog_expr::VExprAst::MakeUnaryParamAst(verilog_expr::voperator::DELAY,
      $1,
      tmp, stmp );
  }
| expression DELAY UNSIGNED_NUMBER  next_sequence  {
    /* e ## M  id or (...) */
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($3));
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1,$4,
      tmp, {""} );
  }
| expression DELAY simple_identifier DOT UNSIGNED_NUMBER next_sequence {
    /* e ## clk.M  id or (...) */
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($5));
    std::vector<std::string> stmp;
    stmp.push_back($3);
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $6,
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET UNSIGNED_NUMBER COLON UNSIGNED_NUMBER CLOSE_SQ_BRACKET next_sequence {
  /*1          2        3                4          5      6               7                8 */
  /* e ## [M:N] id or (...) */
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($4));
    tmp.push_back(verilog_expr::width_to_int($6));
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $8,
      tmp, {"", ""} );
  }
| expression DELAY OPEN_SQ_BRACKET simple_identifier DOT UNSIGNED_NUMBER COLON UNSIGNED_NUMBER CLOSE_SQ_BRACKET next_sequence {
    /*1        2       3              4               5    6                7      8              9              aaaa*/
    /* e ## [clk.M:N] id or (...) */
    std::vector<int> tmp;
    tmp.push_back(verilog_expr::width_to_int($6));
    tmp.push_back(verilog_expr::width_to_int($8));
    std::vector<std::string> stmp;
    stmp.push_back($4);
    stmp.push_back("");
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $10,
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET UNSIGNED_NUMBER COLON simple_identifier DOT UNSIGNED_NUMBER CLOSE_SQ_BRACKET next_sequence {
  /* 1         2      3               4              5      6              777       8           9               10*/
  /* e ## [M:clk.N] id or (...) */
  std::vector<int> tmp;
  tmp.push_back(verilog_expr::width_to_int($4));
  tmp.push_back(verilog_expr::width_to_int($8));
  std::vector<std::string> stmp;
  stmp.push_back("");
  stmp.push_back($6);
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $10, 
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET simple_identifier DOT UNSIGNED_NUMBER COLON simple_identifier DOT UNSIGNED_NUMBER CLOSE_SQ_BRACKET next_sequence {
  /*11111111 22222 333333333333333 44444444444444444 555 666666666666666 77777 88888888888888888 999 aaaaaaaaaaaaaaa bbbbbbbbbbbbbbbb ccccccccccccc*/
  /* e ## [clk.M:clk.N] id or (...) */
  std::vector<int> tmp;
  tmp.push_back(verilog_expr::width_to_int($6));
  tmp.push_back(verilog_expr::width_to_int($10));
  std::vector<std::string> stmp;
  stmp.push_back($4);
  stmp.push_back($8);
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $12,
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET UNSIGNED_NUMBER COLON DOLLAR CLOSE_SQ_BRACKET next_sequence {
  /*11111111 22222 333333333333333 444444444444444 55555 666666 7777777777777777 8888888888888*/
  /* e ## [M:$] id or (...) */
  std::vector<int> tmp;
  tmp.push_back(verilog_expr::width_to_int($4));
  tmp.push_back(0);
  std::vector<std::string> stmp;
  stmp.push_back("");
  stmp.push_back("");
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $8,
      tmp, stmp );
  }
| expression DELAY OPEN_SQ_BRACKET simple_identifier DOT UNSIGNED_NUMBER COLON DOLLAR CLOSE_SQ_BRACKET next_sequence {
  /*11111111 22222 333333333333333 44444444444444444 555 666666666666666 77777 888888 9999999999999999 aaaaaaaaaaaaa*/
  /* e ## [clk.M:$] id or (...) */
  std::vector<int> tmp;
  tmp.push_back(verilog_expr::width_to_int($6));
  tmp.push_back(0);
  std::vector<std::string> stmp;
  stmp.push_back($4);
  stmp.push_back("");
    $$ = verilog_expr::VExprAst::MakeBinaryParamAst(verilog_expr::voperator::DELAY,
      $1, $10,
      tmp, stmp );
  }
;


next_sequence : hierarchical_identifier {
    $$ = verilog_expr::VExprAst::MakeVar($1);
  }
| hierarchical_identifier_special_name {
    $$ = verilog_expr::VExprAst::MakeSpecialName($1);
  }
| number {
    $$ = $1;
  }
| OPEN_BRACKET expression CLOSE_BRACKET {
    $$ = $2;
  }
;

/* A.8.3 Expressions */

conditional_expression : 
  expression TERNARY attribute_instances expression COLON expression{
    $$ = verilog_expr::VExprAst::MakeTernaryAst( verilog_expr::voperator::TERNARY, $1,$4,$6);
  }
;


primary :
  number{
      $$ = $1;
  }
| hierarchical_identifier {
      $$ = verilog_expr::VExprAst::MakeVar($1);
  }
| primary sq_bracket_expression {
    if ( $2.op == verilog_expr::voperator::INDEX ) {
      // binary operation
      $$ = verilog_expr::VExprAst::MakeBinaryAst($2.op, $1, $2.ranges.at(0));
    } else {
      // ternary operation
      $$ = verilog_expr::VExprAst::MakeTernaryAst($2.op, $1, $2.ranges.at(0), $2.ranges.at(1));
    }
  }
| string {$$ = verilog_expr::VExprAst::MakeSpecialName($1);}
| hierarchical_identifier_special_name {
  $$ = verilog_expr::VExprAst::MakeSpecialName($1);
}
| concatenation{
    $$ = $1;
  }
| multiple_concatenation{
    $$ = $1;
  }
| OPEN_BRACKET expression CLOSE_BRACKET{
    $$ = $2;
  }
;



hierarchical_identifier_special_name :
 HASH SIMPLE_ID HASH {
  /* this is #a#, but we return the string in the middle */
  $$ = $2;
  }
;


/* A.8.1 Concatenations */

concatenation : 
  OPEN_SQ_BRACE expressions CLOSE_SQ_BRACE{
   $$ = verilog_expr::VExprAst::MakeNaryAst(verilog_expr::voperator::CONCAT, $2 );
  }
;


multiple_concatenation :
  OPEN_SQ_BRACE expression concatenation CLOSE_SQ_BRACE{
    $$ =  verilog_expr::VExprAst::MakeBinaryAst(verilog_expr::voperator::REPEAT, $2, $3 );
  }
;


number :
  NUM_REAL{
    $$ = verilog_expr::VExprAst::MakeConstant(0,0,$1);
  }
| BIN_BASE BIN_VALUE {
  // TODO : 1. auto width determine
  //        2. width check
  //        3. check?
  // NOTE: you can also add internal translation annotations
  //       when handling this pass
    $$ = verilog_expr::VExprAst::MakeConstant(2, 0 ,$2);
}
| HEX_BASE HEX_VALUE {
    $$ = verilog_expr::VExprAst::MakeConstant(16, 0 ,$2);
}
| OCT_BASE OCT_VALUE {
    $$ = verilog_expr::VExprAst::MakeConstant(8, 0 ,$2);
}
| DEC_BASE UNSIGNED_NUMBER {
    $$ = verilog_expr::VExprAst::MakeConstant(10, 0 ,$2);
}
| UNSIGNED_NUMBER BIN_BASE BIN_VALUE {
    $$ = verilog_expr::VExprAst::MakeConstant(2, verilog_expr::width_to_int($1) ,$3);
}
| UNSIGNED_NUMBER HEX_BASE HEX_VALUE {
    $$ = verilog_expr::VExprAst::MakeConstant(16, verilog_expr::width_to_int($1) ,$3);
}
| UNSIGNED_NUMBER OCT_BASE OCT_VALUE {
    $$ = verilog_expr::VExprAst::MakeConstant(8, verilog_expr::width_to_int($1) ,$3);
}
| UNSIGNED_NUMBER DEC_BASE UNSIGNED_NUMBER{
    $$ = verilog_expr::VExprAst::MakeConstant(10, verilog_expr::width_to_int($1) ,$3);
}
| unsigned_number {
    $$ = verilog_expr::VExprAst::MakeConstant(0,0,$1);}
;


unsigned_number :
  UNSIGNED_NUMBER {
    $$ = $1;
  }
;


function_call : hierarchical_identifier
 attribute_instances OPEN_BRACKET expressions CLOSE_BRACKET{
    ($4).insert(($4).begin(), verilog_expr::VExprAst::MakeVar($1));
    $$ = verilog_expr::VExprAst::MakeNaryAst(verilog_expr::voperator::FUNCTION_APP, $4 );
 }
 |  hierarchical_identifier
 attribute_instances OPEN_BRACKET CLOSE_BRACKET {
   verilog_expr::VExprAst::VExprAstPtrVec tmp;
   tmp.push_back(verilog_expr::VExprAst::MakeVar($1));
   $$ = verilog_expr::VExprAst::MakeNaryAst(verilog_expr::voperator::FUNCTION_APP, tmp );
 }
;


expressions :
  expression {
   $$ = verilog_expr::VExprAst::VExprAstPtrVec();
   ($$).push_back($1);
  }
| expressions COMMA expression{
  $$ = $1;
  ($$).push_back($3);
  }
;



sq_bracket_expression :
  OPEN_SQ_BRACKET expression CLOSE_SQ_BRACKET{
    // create one and replace as needed
    $$ = verilog_expr::SuffixOp();
    ($$).op = verilog_expr::voperator::INDEX;
    ($$).ranges.push_back($2);
  }
| OPEN_SQ_BRACKET expression COLON  expression CLOSE_SQ_BRACKET{
    $$ = verilog_expr::SuffixOp();
    ($$).op = verilog_expr::voperator::RANGE_INDEX;
    ($$).ranges.push_back($2);
    ($$).ranges.push_back($4);
  }
| OPEN_SQ_BRACKET expression IDX_PRT_SEL_PLUS expression CLOSE_SQ_BRACKET{
    $$ = verilog_expr::SuffixOp();
    ($$).op = verilog_expr::voperator::IDX_PRT_SEL_PLUS;
    ($$).ranges.push_back($2);
    ($$).ranges.push_back($4);
  }
| OPEN_SQ_BRACKET expression IDX_PRT_SEL_MINUS expression CLOSE_SQ_BRACKET{
      // $2 $4
    $$ = verilog_expr::SuffixOp();
    ($$).op = verilog_expr::voperator::IDX_PRT_SEL_MINUS;
    ($$).ranges.push_back($2);
    ($$).ranges.push_back($4);
  }
;



string : STRING {$$=$1;} ;

/* A.9.1 Attributes */

attribute_instances : { $$=verilog_expr::Attribute(); }
                    | list_of_attribute_instances { $$=$1; }
                    ;

list_of_attribute_instances : 
  ATTRIBUTE_START attr_specs ATTRIBUTE_END {
      $$ = $2;
  }
| ATTRIBUTE_START attr_specs ATTRIBUTE_END list_of_attribute_instances{
      $$ = $2;
      ($$).Append($4);
  }
;

attr_specs : { $$ = verilog_expr::Attribute(); }
           | attr_name EQ expression {
               // make new one
               $$ = verilog_expr::Attribute();
               ($$).AddAttribute($1,$3);
           }
           | attr_name EQ expression COMMA attr_specs {
               // Append the new item to the existing list and return.
               $$ = $5;
               ($$).AddAttribute($1,$3);               
           }
           ;


attr_name : identifier {$$=$1;};


hierarchical_identifier : 
  simple_identifier {
      $$ = $1;
  }
| hierarchical_identifier DOT simple_identifier{
  // text_macro_usage
      $$ = $1 + "." + $3;
  }
| hierarchical_identifier DOT escaped_identifier{
      $$ = $1 + "." + $3;
  }
;




identifier : 
  simple_identifier  {$$=$1;}
| escaped_identifier {$$=$1;}
| text_macro_usage {$$=$1;}
;


escaped_identifier  : ESCAPED_ID {
    $$=$1;
};



simple_identifier: 
  SIMPLE_ID {
    $$ = $1; /* verilog_expr::VExprAst::MakeVar($1); */
}
;


/* 19.0 Compiler Directives */


text_macro_usage : MACRO_IDENTIFIER {
  $$=$1;
};



/* A.8.6 Operators */

unary_operator : PLUS    {$$ = verilog_expr::voperator::PLUS;}
               | MINUS   {$$ = verilog_expr::voperator::MINUS;}
               | L_NEG   {$$ = verilog_expr::voperator::L_NEG;}
               | B_NEG   {$$ = verilog_expr::voperator::B_NEG;}
               | B_AND   {$$ = verilog_expr::voperator::B_AND;}
               | B_NAND  {$$ = verilog_expr::voperator::B_NAND;}
               | B_OR    {$$ = verilog_expr::voperator::B_OR;}
               | B_NOR   {$$ = verilog_expr::voperator::B_NOR;}
               | B_XOR   {$$ = verilog_expr::voperator::B_XOR;}
               | B_EQU   {$$ = verilog_expr::voperator::B_EQU;}
               ;


%%

// Bison expects us to provide implementation - otherwise linker complains
void Vexp::Parser::error(const location &loc , const std::string &message) {
        
        // Location should be initialized inside scanner action, but is not in this example.
        // Let's grab location directly from driver class.
	// cout << "Error: " << message << endl << "Location: " << loc << endl;
	
        std::cout << "Error: " << message << std::endl << "Error location: " << driver.location() << std::endl;
        driver.SetError();
}
