#include "vexpparser/interpreter.h"

#include <iostream>
#include <sstream>

using namespace std;

int main(int argc, char ** argv) {
  {
    if(argc >= 2) {
      for (int idx = 1; idx < argc; ++idx) {
        
        Vexp::Interpreter intp;
        stringstream ss;
        ss << argv[idx];
        intp.switchInputStream(&ss);
        try{
          intp.parse();
        } catch (verilog_expr::VexpException &e) {
          cout << "AST constructor error:" << e.msg_ << endl;
        }
        cout << intp.str() << endl;
        cout << intp.GetAstRoot()->to_verilog() << endl;
      }
      return 0;
    }
  }

  {
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "i0.a +a.b*4'd8 + (abc+1)@(~t.t0)*a@b##1";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
  {
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "RTL.i1 + (RTL.v2+1)@(#decode#)";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
  { // function
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "RTL.i1 + $abc(RTL.v2+1)@(#decode#)";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }

  { // delay1
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "RTL.i1 ## clk.1 (b+c)";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }

  { // delay2
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "RTL.i1 ## clk.1 (b+c) ##3 c";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
  { // delay 3
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "a ##[clk.1:clk.2] b";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }

  { // delay 4
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "((a ##[clk.1:$] b) ##[1:2] c) ##3 d";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }

  { // delay 5
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "a ##[clk.1:clk.3] b ##[1:clk2.2] c ##clk.3 d";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }

  { // index
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "RTL.i1 ## clk.1 (b[1][2]) ##3";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
  { // imply
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "a |-> b ## 1 c"; // same as "a |-> (b ##1 c)"
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
//-------------------------------------------
  { // concat
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "{(a + b)[2:0], ({c,d})[1:0]}";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
//-------------------------------------------

//-------------------------------------------
  { // array
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "$forall(v:bv8, v<8 |-> a[v]==2)";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
//-------------------------------------------

//-------------------------------------------
  { // array store
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "array:<i1>:v1:<i2>:v2:<i3>:v3:<i4>:v4";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
//-------------------------------------------
//-------------------------------------------
  { // array store2
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "array:<i1>:v1+2"; // v1+2 is associated tighter
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
  }
//-------------------------------------------

  cout << "-----------------------------\n";
  std::string st;
  {
    Vexp::Interpreter intp;
    stringstream ss;
    ss << "i0.a +{a.b*4'd8,23} + (abc+1)/(~t.t0)*a-b(1,5^'h5)";
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
    st = intp.GetAstRoot()->to_verilog();
    cout << st << endl;
  }
  {
    Vexp::Interpreter intp;
    stringstream ss;
    ss << st;
    intp.switchInputStream(&ss);
    try{
      intp.parse();
    } catch (verilog_expr::VexpException &e) {
      cout << "AST constructor error:" << e.msg_ << endl;
    }
    cout << intp.str() << endl;
    st = intp.GetAstRoot()->to_verilog();
    cout << st << endl;
  }

  

  return 0;
}
