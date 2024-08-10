// Header for AST nodes
// Hongce Zhang (hongcez@princeton.edu)

#ifndef _VEXPPARSER_VEXP_H_
#define _VEXPPARSER_VEXP_H_

#include <memory>
#include <vector>
#include <string>
#include <iostream>
#include <unordered_map>

namespace verilog_expr {

enum class ExceptionCause { 
  OpNaryNotMatched, //
  OpNaryNotMatchedVlgTranslation, //
  UntranslatedVerilog,
  UnknownVlgTranslation,
  UntranslatedSmtlib2,
  UnknownNumberVlgTranslation,
  UnknownNumberSmtTranslation,
  TypeMismatch
};

class VexpException {
public:
  VexpException( ExceptionCause cause, const std::string & msg = "" ) : cause_ ( cause ), msg_(msg) {}

  const ExceptionCause cause_;
  const std::string msg_;
};

// map: operator -> to their string name 
extern std::vector<std::string> voperator_str_vec;

enum class voperator { 
  STAR, // mul
  PLUS,
  MINUS,
  ASL,
  ASR,
  LSL,
  LSR,
  DIV,
  POW,
  MOD,
  GTE,
  LTE,
  GT,
  LT,
  L_NEG,
  L_AND,
  L_OR,
  C_EQ,
  L_EQ,
  C_NEQ,
  L_NEQ,
  B_NEG,
  B_AND,
  B_OR,
  B_XOR,
  B_EQU,
  B_NAND,
  B_NOR,
  INDEX, // [idx] operator  A[i1][i2] -> index(index(A,i1),i2)   A[i1[i2]]  index(A, index(i1,i2))
  RANGE_INDEX, // [i1:i2] ternary
  IDX_PRT_SEL_PLUS, // [i1:+i2] ternary
  IDX_PRT_SEL_MINUS, // [i1:-i2] ternary
  STORE_OP, // A:<3>:5:<4>:6:<5>:7  (not supported yet)
  AT,

  TERNARY,
  /*special ops*/
  FUNCTION_APP,
  CONCAT,
  REPEAT,
  /*Placeholder*/
  MK_CONST,
  MK_VAR,

  /*Add new ones here*/
  DELAY

   };

class AbstractInternalInfo {
  // this class can be used to attach additional information
  // to an ast node and generally, you should create
  // derived class from it
  public:
    typedef std::shared_ptr<AbstractInternalInfo> InternalInfoPtr;
    virtual void should_not_instantiate() = 0;
    virtual bool translatable() {return true;}
}; 

class VExprAst {
public:
  using InternalInfoPtr = AbstractInternalInfo::InternalInfoPtr;
  typedef std::shared_ptr<VExprAst> VExprAstPtr;
  typedef std::vector<VExprAstPtr> VExprAstPtrVec;
  
  voperator get_op() { return op_; }
  unsigned get_child_cnt() { return child_.size() ; }
  virtual const VExprAstPtrVec & get_child()  { return child_; } 
  // VExprAstPtr & child(unsigned idx)  { return child_.at(idx); }
  // about the annotation
  template<class T> std::shared_ptr<T> get_annotation() const {
    return annotate_ == nullptr ? nullptr : std::dynamic_pointer_cast<T>(annotate_);
  }
  void set_annotation(const InternalInfoPtr & anno) { annotate_ = anno; }

  const std::vector<int> & get_parameter() const { return parameter_; }
  const std::vector<std::string> & get_str_parameter() const { return str_parameter_; }

  // factory function -- do the checking here
  virtual VExprAstPtr MakeCopyWithNewChild(const VExprAstPtrVec& in) const;
  
  static VExprAstPtr MakeConstant(int base, int width, const std::string & lit); // if no width specified then 0
  static VExprAstPtr MakeSpecialName(const std::string & name); // # name #
  static VExprAstPtr MakeVar(const std::string & name); // hierarchy names?
  static VExprAstPtr MakeUnaryAst(voperator op, const VExprAstPtr & c);
  static VExprAstPtr MakeUnaryParamAst(voperator op, const VExprAstPtr & c, const std::vector<int> & param, const std::vector<std::string> & sparam);
  static VExprAstPtr MakeBinaryParamAst(voperator op, const VExprAstPtr & c1, const VExprAstPtr & c2, const std::vector<int> & param, const std::vector<std::string> & sparam);
  
  
  static VExprAstPtr MakeBinaryAst(voperator op, const VExprAstPtr & c1, const VExprAstPtr & c2);
  static VExprAstPtr MakeTernaryAst(voperator op, const VExprAstPtr & c1, const VExprAstPtr & c2, const VExprAstPtr & c3);
  static VExprAstPtr MakeNaryAst(voperator op, const VExprAstPtrVec & children);
  
  friend std::ostream & operator<<(std::ostream & os, const VExprAstPtr & obj);
  
  virtual bool is_leaf()     const { return false; }
  virtual bool is_var()      const { return false; }
  virtual bool is_constant() const { return false; }
  virtual std::string to_verilog() const;

  VExprAst(voperator op, const VExprAstPtrVec & c, 
    const std::vector<int> & parameter, const std::vector<std::string> & str_parameter) : 
        op_(op) , child_(c), parameter_(parameter), str_parameter_(str_parameter)  {}

protected:
  // unmutable
  const voperator op_;
  const VExprAstPtrVec child_;
  const std::vector<int> parameter_;
  const std::vector<std::string> str_parameter_;
  
  InternalInfoPtr annotate_;
};


class Attribute {
  using VExprAstPtr = VExprAst::VExprAstPtr;
public:
  typedef std::shared_ptr<Attribute> AttributePtr;
  typedef std::unordered_map<std::string,VExprAstPtr> AttribMapT;

  Attribute() {}
  bool AddAttribute(const std::string & name, const VExprAstPtr & exp);
  void Append(const Attribute & other);
protected:
  AttribMapT attrib_;
};

class VExprAstConstant : public VExprAst{
  friend class VExprAst;
public:
  typedef std::shared_ptr<VExprAstConstant> VExprAstConstantPtr;
  static inline VExprAstConstantPtr cast_ptr(const VExprAstPtr & in) { return std::dynamic_pointer_cast<VExprAstConstant>(in); }
  
  virtual bool is_leaf()     const override {return true;}
  virtual bool is_constant() const override {return true;}
  
  virtual VExprAstPtr MakeCopyWithNewChild(const VExprAstPtrVec& in) const;
  
  std::tuple<int, int, std::string> get_constant() const {return std::make_tuple(base_, width_, lit_);}

  virtual std::string to_verilog() const override;

  VExprAstConstant(int base, int width, const std::string & lit) :
     VExprAst(voperator::MK_CONST, {}, {}, {}), base_(base), width_(width), lit_ (lit) {}

protected:
  int base_; // 0 (real number) , 2,4,8, 10,16
  int width_;
  std::string lit_; // the actual number part
};

class VExprAstVar : public VExprAst {
  friend class VExprAst;
public:
  typedef std::shared_ptr<VExprAstVar> VExprAstVarPtr;
  static inline VExprAstVarPtr cast_ptr(const VExprAstPtr & in) { return std::dynamic_pointer_cast<VExprAstVar>(in); }
  
  virtual bool is_leaf() const override {return true;}
  virtual bool is_var()  const override {return true;}
  
  virtual VExprAstPtr MakeCopyWithNewChild(const VExprAstPtrVec& in) const;
  
  std::pair<std::string,bool> get_name() const {return std::make_pair(name_,is_special_name_);}
  
  virtual std::string to_verilog() const override;

  VExprAstVar(const std::string & name, bool is_special_name) : 
    VExprAst(voperator::MK_VAR, {}, {}, {}), 
    name_(name), is_special_name_(is_special_name) {}

protected:
  std::string name_;
  bool is_special_name_; // #name#
};

int width_to_int(const std::string &); // convert width to int

// this class is only used in AST construction
struct SuffixOp {
  using VExprAstPtr = VExprAst::VExprAstPtr;

  voperator op;
  std::vector<VExprAstPtr> ranges;
}; // SuffixOp

} // namespace verilog_expr

#endif // _VEXPPARSER_VEXP_H_
