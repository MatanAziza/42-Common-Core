/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_stack.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 13:13:54 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/19 18:04:10 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_STACK_H
# define FT_STACK_H

# include "ft_output.h"
// Double linked list node.
// Includes an idx field that represents
// a discretized (normalized) value representing
// the value as it's index in the sorted list.
typedef struct s_node
{
	struct s_node	*next;
	struct s_node	*previous;
	unsigned long	idx;
	long			value;
}					t_node;

// A simple marker for the name of the stack.
typedef enum e_stack_name
{
	A,
	B
}					t_stack_name;

// An enum pointing whether rotating or reverse-rotating is the better choice.
typedef enum e_position
{
	R,
	RR,
}					t_position;
// A general representation of our stack. It links under the hood to a doubly
// linked list.
typedef struct s_stack
{
	t_node			*head;
	t_node			*tail;
	unsigned long	size;
	t_stack_name	name;
}					t_stack;

// List of operations on nodes :
// -----------------------------

// Creates a new node to store in a stack.
t_node				*new_stack_member(long value);
void				stack_add_back(t_stack *stack, t_node *node);
void				stack_add_front(t_stack *stack, t_node *node);
// Removes a node from a stack and gives back to the caller the
// reference to the now orphaned node. It needs to be re-added
// to a `t_stack` to prevent memory leaks.
t_node				*take(t_stack *stack);
// Clones and initializes a single node from the double linked list.
// It returns a null pointer if the allocation fails.
t_node				*clone_unlinked_node(t_node *source);
// List of operations on stacks :
// ------------------------------

// This function should take a stack-allocated outer pointer `stack`; it will
//  free the inner ptr, but not the outer one.
// If you use this with a malloc `stack` ptr, free the outer ptr yourself.
t_stack				*new_stack(t_stack_name name);
// This function clones a stack and it's associated linked list ; if
// the stack fails to allocate, it returns a null pointer. If a node
// of the list fails to allocate, it returns early with an incomplete
// but properly formed stack.
t_stack				*clone_stack(t_stack *origin);
void				clear_stack(t_stack **stack);
// The `push` operation on a stack. It takes a value from the stack `from` and
// prepends it on the stack `to`. Does nothing on empty stacks.
void				push(t_stack *from, t_stack *to, t_output *out);
// The `rotate` operation on a stack. It keeps the underlying structure exactly
// the same, but changes where `head` and `tail` are on the circular list.
void				rotate(t_stack *stack, t_output *out);
// The `reverse rotate` operation on a stack. It keeps the underlying
// structure exactly the same, but changes where `head` and `tail` are on the
// circular list.
void				reverse_rotate(t_stack *stack, t_output *out);
// The `swap` operation on a stack. It changes the position of the two first
// elements of the list.
void				swap(t_stack *stack, t_output *out);

#endif
