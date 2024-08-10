// Source for AST nodes

#include <vexpparser/vexp.h>
#include <cassert>

namespace verilog_expr {

// warning : will not make copy of annotation!
VExprAst::VExprAstPtr VExprAst::MakeCopyWithNewChild(const VExprAstPtrVec& in) const {
  assert(in.size() == child_.size());
  auto ret = std::make_shared<VExprAst>(op_ , in, parameter_, str_parameter_);
  return ret;
}
VExprAst::VExprAstPtr VExprAstVar::MakeCopyWithNewChild(const VExprAstPtrVec& in) const {
  assert(in.empty());
  if(is_special_name_)
    return MakeSpecialName(name_);
  return MakeVar(name_);
}

VExprAst::VExprAstPtr VExprAstConstant::MakeCopyWithNewChild(const VExprAstPtrVec& in) const {
  assert(in.empty());
  auto ret = MakeConstant(base_, width_, lit_);
  return ret;
}


VExprAst::VExprAstPtr VExprAst::MakeConstant(int base, int width, const std::string & lit) {
  return std::make_shared<VExprAstConstant>(base, width, lit);
}

// # name #
VExprAst::VExprAstPtr VExprAst::MakeSpecialName(const std::string & name) {
  return std::make_shared<VExprAstVar>(name, true);
}
VExprAst::VExprAstPtr VExprAst::MakeVar(const std::string & name) {
  return std::make_shared<VExprAstVar>(name, false);
}

VExprAst::VExprAstPtr VExprAst::MakeUnaryAst(voperator op, const VExprAstPtr & c) {
  if (op == voperator::PLUS ||
      op == voperator::MINUS  ||
      op == voperator::L_NEG  ||
      op == voperator::B_NEG  ||
      op == voperator::B_AND  ||
      op == voperator::B_NAND ||
      op == voperator::B_OR   ||
      op == voperator::B_NOR  ||
      op == voperator::B_XOR  ||
      op == voperator::B_EQU      // "^~"|"~^"
    ) {
    VExprAstPtrVec tmp({c});
    return std::make_shared<VExprAst>(op , tmp,
      std::vector<int>({}), std::vector<std::string>({}) );
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "N-ary not matched in MakeUnaryAst");
  return NULL;
}

VExprAst::VExprAstPtr VExprAst::MakeQuantifiedExpr(voperator op, const std::string & quantified_name, 
    unsigned qwidth, const VExprAstPtr & quantified_expr) {
  if(op == voperator::FORALL || op == voperator::EXIST ) {
    VExprAstPtrVec tmp({quantified_expr});
    const std::vector<int> param({int(qwidth)});
    const std::vector<std::string> sparam ({quantified_name});
    return std::make_shared<VExprAst>(op, tmp, param, sparam);
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "expect forall or exist");
  return NULL;
}


VExprAst::VExprAstPtr VExprAst::MakeUnaryParamAst(voperator op, const VExprAstPtr & c, const std::vector<int> & param, const std::vector<std::string> & sparam) {
  if (op == voperator::DELAY     // "^~"|"~^"
    ) {
    VExprAstPtrVec tmp({c});
    auto tmpptr = std::make_shared<VExprAst>(op , tmp, param, sparam);
    return tmpptr;
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "N-ary not matched in MakeUnaryParamAst");
  return NULL;
}


VExprAst::VExprAstPtr VExprAst::MakeBinaryParamAst(voperator op, const VExprAstPtr & c1, const VExprAstPtr & c2, const std::vector<int> & param, const std::vector<std::string> & sparam) {
  if (op == voperator::DELAY     // "^~"|"~^"
    ) {
    VExprAstPtrVec tmp({c1, c2});
    auto tmpptr = std::make_shared<VExprAst>(op , tmp, param, sparam);
    return tmpptr;
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "N-ary not matched in MakeUnaryParamAst");
  return NULL;
}

VExprAst::VExprAstPtr VExprAst::MakeBinaryAst(voperator op, const VExprAstPtr & c1, const VExprAstPtr & c2) {
  if (op == voperator::REPEAT     || // {x{a}}
      op == voperator::STAR       || // mul
      op == voperator::PLUS       ||
      op == voperator::MINUS      ||
      op == voperator::ASL        ||
      op == voperator::ASR        ||
      op == voperator::LSL        ||
      op == voperator::LSR        ||
      op == voperator::DIV        ||
      op == voperator::POW        ||
      op == voperator::MOD        ||
      op == voperator::GTE        ||
      op == voperator::LTE        ||
      op == voperator::GT         ||
      op == voperator::LT         ||
      op == voperator::L_NEG      ||
      op == voperator::L_AND      ||
      op == voperator::L_OR       ||
      op == voperator::C_EQ       ||
      op == voperator::L_EQ       ||
      op == voperator::C_NEQ      ||
      op == voperator::L_NEQ      ||
      op == voperator::B_NEG      ||
      op == voperator::B_AND      ||
      op == voperator::B_OR       ||
      op == voperator::B_XOR      ||
      op == voperator::B_EQU      ||
      op == voperator::B_NAND     ||
      op == voperator::B_NOR      ||

      op == voperator::INDEX      ||
      op == voperator::AT
    ) {
    VExprAstPtrVec tmp({c1,c2});
    return std::make_shared<VExprAst>(op , tmp,
      std::vector<int>({}), std::vector<std::string>({}) );
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "N-ary not matched in MakeBinaryAst");
  return NULL;
}


VExprAst::VExprAstPtr VExprAst::MakeTernaryAst(voperator op, const VExprAstPtr & c1, const VExprAstPtr & c2, const VExprAstPtr & c3) {
  if (op == voperator::TERNARY || 
      op == voperator::RANGE_INDEX ||
      op == voperator::IDX_PRT_SEL_PLUS ||
      op == voperator::IDX_PRT_SEL_MINUS ||
      op == voperator::STORE_OP
    ) {
    VExprAstPtrVec tmp({c1,c2,c3});
    return std::make_shared<VExprAst>(op , tmp,
      std::vector<int>({}), std::vector<std::string>({}) );
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "N-ary not matched in MakeTernaryAst");
  return NULL;
}

VExprAst::VExprAstPtr VExprAst::MakeNaryAst(voperator op, const VExprAstPtrVec & children) {
  // function application & concat 
  if (op == voperator::FUNCTION_APP || 
      op == voperator::CONCAT
    ) {
    return std::make_shared<VExprAst>(op , children,
      std::vector<int>({}), std::vector<std::string>({}) );
  }
  throw VexpException(ExceptionCause::OpNaryNotMatched, "N-ary not matched in MakeNaryAst");
  return NULL;
}

std::vector<std::string> voperator_str_vlg = {
  "*", // STAR
  "+",
  "-",
  "<<<",
  ">>>",
  "<<",
  ">>",
  "/",
  "**",
  "%",
  ">=",
  "<=",
  ">",
  "<",
  "!",
  "&&",
  "||",
  "===",
  "==",
  "!==",
  "!=",
  "~",
  "&",
  "|",
  "^",
  "~^",
  "~&",
  "~|", // B_NOR
  "#special", // [idx] operator  A[i1][i2] -> index(index(A,i1),i2)   A[i1[i2]]  index(A, index(i1,i2))
  ":", // [i1:i2] ternary
  ":+", // [i1:+i2] ternary
  ":-", // [i1:-i2] ternary
  "#notsupported", // A:<3>:5:<4>:6:<5>:7  (not supported yet)
  "#notsupported",
  "?", // ternary
  /*special ops*/
  "#special",
  "#special",
  "#special",
  /*Placeholder*/
  "MK_CONST",
  "MK_VAR",

  "#notsupported", // delay
  "#notsupported", // forall
  "#notsupported"  // exist
};


std::string VExprAstVar::to_verilog() const {
  if(annotate_.get() != nullptr && !(annotate_->translatable()) )
    throw VexpException(ExceptionCause::UntranslatedVerilog, name_ );
  return name_;
}


std::string VExprAstConstant::to_verilog() const {
  if(base_ == 0 && width_ != 0)
    throw VexpException(ExceptionCause::UnknownNumberVlgTranslation , "base_ == 0 && width_ != 0" ); 
  
  if(base_ == 0 && width_ == 0)
    return lit_;
  
  std::string ret;
  if(width_ != 0) // base != 0
    ret = std::to_string(width_);
  ret += "'";

  switch(base_) {
    case 2: ret += "b"; break;
    case 8: ret += "o"; break;
    case 10: ret += "d"; break;
    case 16: ret += "h"; break;
    default: throw VexpException(ExceptionCause::UnknownNumberVlgTranslation , "base" );
  }
  return ret+lit_; 
}

std::string VExprAst::to_verilog() const {
  assert(op_ != voperator::MK_CONST && op_ != voperator::MK_CONST);

  unsigned idx = static_cast<unsigned>(op_);
  assert(idx < voperator_str_vlg.size());
  auto opstr = voperator_str_vlg.at(idx);
  if (opstr == "#notsupported")
    throw VexpException(ExceptionCause::UntranslatedVerilog, opstr );

  if ( child_.size() == 1 &&
      (op_ == voperator::PLUS ||
      op_ == voperator::MINUS  ||
      op_ == voperator::L_NEG  ||
      op_ == voperator::B_NEG  ||
      op_ == voperator::B_AND  ||
      op_ == voperator::B_NAND ||
      op_ == voperator::B_OR   ||
      op_ == voperator::B_NOR  ||
      op_ == voperator::B_XOR  ||
      op_ == voperator::B_EQU      // "^~"|"~^"
    ) ) {
    return opstr+"("+ child_.at(0)->to_verilog() +")";
  }

  // binary or more
  switch(op_) {
    case voperator::STAR: // mul
    case voperator::PLUS:
    case voperator::MINUS:
    case voperator::ASL:
    case voperator::ASR:
    case voperator::LSL:
    case voperator::LSR:
    case voperator::DIV:
    case voperator::POW:
    case voperator::MOD:
    case voperator::GTE:
    case voperator::LTE:
    case voperator::GT:
    case voperator::LT:
    case voperator::L_AND:
    case voperator::L_OR:
    case voperator::C_EQ:
    case voperator::L_EQ:
    case voperator::C_NEQ:
    case voperator::L_NEQ:
    case voperator::B_AND:
    case voperator::B_OR:
    case voperator::B_XOR:
    case voperator::B_EQU:
    case voperator::B_NAND:
    case voperator::B_NOR:
      if(child_.size()!=2)
        throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, opstr );
      return  "("+ child_.at(0)->to_verilog() + ")" + opstr + "("+ child_.at(1)->to_verilog()  + ")";
      break;
    default:
      break; // will handle in the following cases
  }

  if(op_ == voperator::INDEX) {
    if(child_.size()!=2)
      throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, opstr );
    // if(!child_.at(0)->is_var())
    //  throw VexpException(ExceptionCause::UntranslatedVerilog, child_.at(0)->to_verilog() + "[" + child_.at(1)->to_verilog() +"]" );
    return child_.at(0)->to_verilog() + "[" + child_.at(1)->to_verilog() +"]" ;
  }

  if (op_ == voperator::RANGE_INDEX || 
      op_ == voperator::IDX_PRT_SEL_PLUS ||
      op_ == voperator::IDX_PRT_SEL_MINUS) {
    if(child_.size()!=3)
      throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, opstr );
    return child_.at(0)->to_verilog() + "[" + child_.at(1)->to_verilog() + opstr + child_.at(2)->to_verilog() +"]" ;
  }

  if (op_ == voperator::TERNARY) {
    if(child_.size()!=3)
      throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, opstr );
    return "("+ child_.at(0)->to_verilog() + ")?(" + child_.at(1)->to_verilog() + "):(" + child_.at(2)->to_verilog() +")" ;
  }

  if (op_ == voperator::CONCAT) {
    if(child_.size() == 0)
      throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, "CONCAT 0 arg" );
    if(child_.size() == 1)
      return child_.at(0)->to_verilog();
    auto str = "{" + child_.at(0)->to_verilog();
    for(size_t idx = 1; idx < child_.size(); ++ idx)
      str += ("," + child_.at(idx)->to_verilog());
    str+="}";
    return str;
  }
  if (op_ == voperator::REPEAT) {
    if(child_.size() == 2)
      throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, "REPEAT not 2-arg" );
    return "{" + child_.at(0)->to_verilog() + child_.at(1)->to_verilog()+"}";
  }
  if (op_ == voperator::FUNCTION_APP) {
    if(child_.size() == 0)
      throw VexpException(ExceptionCause::OpNaryNotMatchedVlgTranslation, "FUNCTION_APP 0 arg" );
    auto funcname = child_.at(0)->to_verilog();
    if (child_.size() == 1)
      return funcname + "()";
    auto param = child_.at(1)->to_verilog();
    for(size_t idx = 2; idx < child_.size(); ++ idx)
      param += ("," + child_.at(idx)->to_verilog());
    return funcname+"("+param+")";   
  }
  throw VexpException(ExceptionCause::UnknownVlgTranslation, opstr );
  return "";
} // translation to verilog


std::vector<std::string> voperator_str_vec = {
  "STAR", // mul
  "PLUS",
  "MINUS",
  "ASL",
  "ASR",
  "LSL",
  "LSR",
  "DIV",
  "POW",
  "MOD",
  "GTE",
  "LTE",
  "GT",
  "LT",
  "L_NEG",
  "L_AND",
  "L_OR",
  "C_EQ",
  "L_EQ",
  "C_NEQ",
  "L_NEQ",
  "B_NEG",
  "B_AND",
  "B_OR",
  "B_XOR",
  "B_EQU",
  "B_NAND",
  "B_NOR",
  "INDEX", // [idx] operator  A[i1][i2] -> index(index(A,i1),i2)   A[i1[i2]]  index(A, index(i1,i2))
  "RANGE_INDEX", // [i1:i2] ternary
  "IDX_PRT_SEL_PLUS", // [i1:+i2] ternary
  "IDX_PRT_SEL_MINUS", // [i1:-i2] ternary
  "STORE_OP", // A:<3>:5:<4>:6:<5>:7  (not supported yet)
  "AT",
  "TERNARY",
  /*special ops*/
  "FUNCTION_APP",
  "CONCAT",
  "REPEAT",
  /*Placeholder*/
  "MK_CONST",
  "MK_VAR",

  "DELAY",
  "FORALL",
  "EXIST"
};

std::ostream & operator<<(std::ostream & os, const VExprAst::VExprAstPtr & obj) {
  if (obj) {
    unsigned idx = static_cast<unsigned>( obj->get_op() );
    os << "(";
    if (idx < voperator_str_vec.size())
      os << voperator_str_vec.at(idx);
    else
      os << "unknown_op";
    os << " ";

    if (! (obj->parameter_.empty())) {
      for (const auto & p : obj->parameter_)
        os << ":"<<p<<" ";
    }

    if (! (obj->str_parameter_.empty())) {
      for (const auto & p : obj->str_parameter_)
        os << "s:"<<p<<" ";
    }

    if (obj->is_var()) {
      auto vptr = VExprAstVar::cast_ptr(obj);
      assert(vptr);
      bool spec = vptr->get_name().second;
      os << (spec?"#":"")  << vptr->get_name().first  << (spec?"#":"")  ;
    } else if (obj->is_constant()) {
      auto cptr = VExprAstConstant::cast_ptr(obj);
      assert(cptr);
      int base; int width; std::string lit;
      std::tie(base, width, lit) = cptr->get_constant();
      os << "base" << base << ",width" << width <<"," << lit;
    } else {
      // traverse the child
      for (const auto & child : obj->get_child())
        os << child <<" ";
    }

    return os << ")";
  }
  // else
  return (os << "(NULL)");
} // operator<<

// -----------------------------------------------------------------


bool Attribute::AddAttribute(const std::string & name, const VExprAstPtr & exp) {
  bool not_overwrite = attrib_.find(name) == attrib_.end();
  attrib_.insert(std::make_pair(name, exp));
  return not_overwrite;
}

void Attribute::Append(const Attribute & other) {
  for (const auto & n_v_pair : other.attrib_) {
    attrib_.insert(std::make_pair(n_v_pair.first, n_v_pair.second));
  }
}


int width_to_int(const std::string & s) { // convert width to int
  try {
    return std::stoi(s, NULL, 10);
  } catch (const std::exception& e) {
    throw VexpException(ExceptionCause::StrToInvFailed, s);
  }
}
int extract_width(const std::string &s ) {
  if(s.length() < 3 || s.find("bv") != 0) {
    throw VexpException(ExceptionCause::ExpectBvXType, s);
  }
  return width_to_int(s.substr(2));
}

} // namespace verilog_expr
