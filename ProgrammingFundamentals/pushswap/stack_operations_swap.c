/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_operations_swap.c                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 19:30:04 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:30:15 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"

static void	swap_for_two(t_stack *s)
{
	t_node	*a;
	t_node	*b;

	a = s->head;
	b = s->tail;
	s->head = b;
	s->tail = a;
	s->head->next = a;
	s->tail->next = b;
	s->head->previous = a;
	s->tail->previous = b;
}

static void	swap_for_any(t_stack *s)
{
	t_node	*a;
	t_node	*b;
	t_node	*c;
	t_node	*t;

	a = s->head;
	b = a->next;
	c = b->next;
	t = s->tail;
	b->previous = t;
	b->next = a;
	a->previous = b;
	a->next = c;
	t->next = b;
	c->previous = a;
	s->head = b;
}

void	swap(t_stack *s, t_output *out)
{
	t_operation	op;

	if (s->size < 2)
		return ;
	if (s->size == 2)
		swap_for_two(s);
	else
		swap_for_any(s);
	if (s->name == A)
		op = OP_SA;
	else
		op = OP_SB;
	if (out)
		output_add_back(out, op);
}
