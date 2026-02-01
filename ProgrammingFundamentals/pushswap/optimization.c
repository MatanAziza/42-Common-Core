/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   optimization.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 13:13:04 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:32:02 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// ra rra  →  (delete both)
// rra ra  →  (delete both)
//
// rb rrb  →  (delete both)
// rrb rb  →  (delete both)
//
// sa sa  →  (delete both)
// sb sb  →  (delete both)
//
//
// pa pb → (delete both)
// pb pa → (delete both)
//
// sa + sb  → ss
// sb + sa  → ss
// ra + rb  → rr
// rb + ra  → rr
// rra + rrb  → rrr
// rrb + rra  → rrr
// [ Linked List Layer ]
//         ↓
// [ Stack Operation VM ]
//         ↓
// [ Algorithm Layer ]
//         ↓
// [ Optional Optimizer ]
//         ↓
// [ Final printing ]
//

#include "ft_algorithms.h"
#include "ft_stack.h"

void	set_idx(t_stack *stack, long value, unsigned long idx)
{
	unsigned long	i;
	t_node			*node;

	i = 0;
	node = stack->head;
	while (i < stack->size)
	{
		if (node->value == value)
		{
			node->idx = idx;
			break ;
		}
		node = node->next;
		i++;
	}
}

// Adds indexing to values ; also checks for duplicates.
t_error	treat_indexing(t_stack *sorted, t_stack *unsorted)
{
	unsigned long	i;
	t_node			*node;

	i = 0;
	node = sorted->head;
	while (i < sorted->size)
	{
		set_idx(unsorted, node->value, i);
		node = node->next;
		i++;
	}
	i = 0;
	node = sorted->head;
	while (i < sorted->size)
	{
		if (node->next)
		{
			if (node->value == node->next->value && node->next != node)
				return (1);
		}
		node = node->next;
		i++;
	}
	return (0);
}

t_error	normalize_values(t_stack *stack)
{
	t_stack	*clone;
	t_stack	*b;
	t_error	err;

	clone = clone_stack(stack);
	b = new_stack(B);
	if (clone && b)
	{
		slow_radix_sort(clone, b, 0, 64);
		if (clone->head && clone->head->previous
			&& clone->head->previous->value < 0)
		{
			reverse_rotate(clone, 0);
			while (clone->tail->value < 0)
				reverse_rotate(clone, 0);
		}
		err = treat_indexing(clone, stack);
	}
	else
		err = 1;
	clear_stack(&clone);
	clear_stack(&b);
	return (err);
}

void	optimize_ops(t_output *out)
{
	optimize_cancel(out);
	optimize_combine(out);
}
