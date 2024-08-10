class node:
	def __init__(self, node_type, left, right):
		self.node_type = node_type
		self.left = left  # None if no left child
		self.right = right # None if no right  child

# Check if two trees are identical:
# have the same structure, and have the same node_type for each node
# we assume ((root1 is not None) and (root2 is not None))
def is_the_same_tree(root1 : node, root2 : node) -> bool:
	if((root1 == None) and (root2 == None)): 
		return True
	elif((root1 != None) and (root2 == None)): 
		return False
	elif((root1 == None) and (root2 != None)): 
		return False
	elif ((root1.node_type == None) and (root2.node_type == None)): 
		return True
	elif((root1.node_type != None) and (root2.node_type == None)): 
		return False
	elif((root1.node_type == None) and (root2.node_type != None)): 
		return False
	
	if(root1.node_type == root2.node_type):	
			return is_the_same_tree(root1.left, root2.left) and is_the_same_tree(root1.right, root2.right)
	else:
		return False

    
    		
    		


print ( is_the_same_tree( node(1,None, None) , node(2,None, None) ) ) # false

print ( is_the_same_tree( node(1,None, None) , node(1,None, None) ) ) # true


print ( is_the_same_tree( node(1,node(1,None,None), node(1,None,None)) , node(1,node(1,None,None), node(1,None,None)) ) ) # true

print ( is_the_same_tree( node(1,node(1,node(1,None,None),None), node(1,None,None)) , node(1,node(1,None,None), node(1,None,None)) ) ) # false

print ( is_the_same_tree( node(1,node(1,node(1,None,None),None), node(2,None,None)) , node(1,node(1,node(1,None,None),None), node(1,None,None)) ) ) # false

print ( is_the_same_tree( node(1,node(1,None,None), node(2,None,None)) , node(1,node(1,None,None), node(1,None,None)) ) ) # false

# add more tests yourself !

