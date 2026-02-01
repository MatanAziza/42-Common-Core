/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   optimization_utils.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 19:31:55 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:33:46 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"

int	find_max_bit(unsigned long value)
{
	int	size;

	size = 0;
	while (value)
	{
		size++;
		value = value >> 1;
	}
	return (size);
}

t_position	order_rotation(t_stack *stack, unsigned long idx)
{
	t_node			*next;
	unsigned long	index;

	next = stack->head;
	index = 0;
	while (index <= (stack->size) / 2)
	{
		if (next->idx == idx)
			return (R);
		next = next->next;
		index++;
	}
	return (RR);
}

const char	*op_str(t_operation op)
{
	if (op == OP_SA)
		return ("sa");
	if (op == OP_SB)
		return ("sb");
	if (op == OP_SS)
		return ("ss");
	if (op == OP_RA)
		return ("ra");
	if (op == OP_RB)
		return ("rb");
	if (op == OP_RR)
		return ("rr");
	if (op == OP_PA)
		return ("pa");
	if (op == OP_PB)
		return ("pb");
	if (op == OP_RRA)
		return ("rra");
	if (op == OP_RRB)
		return ("rrb");
	if (op == OP_RRR)
		return ("rrr");
	return ("ERROR");
}
