/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_actions.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 19:28:34 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:29:17 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"

void	stack_add_back(t_stack *stack, t_node *node)
{
	if (stack->size == 0)
	{
		node->next = node;
		node->previous = node;
		stack->head = node;
		stack->tail = node;
	}
	else
	{
		node->next = stack->head;
		node->previous = stack->tail;
		stack->tail->next = node;
		stack->head->previous = node;
		stack->tail = node;
	}
	stack->size++;
}

void	stack_add_front(t_stack *stack, t_node *node)
{
	if (stack->size == 0)
	{
		node->next = node;
		node->previous = node;
		stack->head = node;
		stack->tail = node;
	}
	else
	{
		node->next = stack->head;
		node->previous = stack->tail;
		stack->tail->next = node;
		stack->head->previous = node;
		stack->head = node;
	}
	stack->size++;
}

t_node	*take(t_stack *from)
{
	t_node	*n;
	t_node	*next;
	t_node	*prev;

	n = from->head;
	if (from->size == 0)
		return (0);
	if (from->size == 1)
	{
		from->head = 0;
		from->tail = 0;
	}
	else
	{
		next = n->next;
		prev = n->previous;
		prev->next = next;
		next->previous = prev;
		from->head = next;
	}
	from->size--;
	n->next = 0;
	n->previous = 0;
	return (n);
}
