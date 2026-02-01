/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_operations.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 15:17:49 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:30:12 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"

void	push(t_stack *from, t_stack *to, t_output *out)
{
	t_node		*ptr;
	t_operation	op;

	ptr = take(from);
	stack_add_front(to, ptr);
	if (to->name == A)
		op = OP_PA;
	else
		op = OP_PB;
	if (out)
		output_add_back(out, op);
}

void	rotate(t_stack *stack, t_output *out)
{
	t_operation	op;

	if (stack->size < 2)
		return ;
	stack->head = stack->head->next;
	stack->tail = stack->tail->next;
	if (stack->name == A)
		op = OP_RA;
	else
		op = OP_RB;
	if (out)
		output_add_back(out, op);
}

void	reverse_rotate(t_stack *stack, t_output *out)
{
	t_operation	op;

	if (stack->size < 2)
		return ;
	stack->head = stack->head->previous;
	stack->tail = stack->tail->previous;
	if (stack->name == A)
		op = OP_RRA;
	else
		op = OP_RRB;
	if (out)
		output_add_back(out, op);
}
