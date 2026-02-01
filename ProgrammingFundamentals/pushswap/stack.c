/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 18:44:03 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/19 18:04:53 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"
#include <stdlib.h>

t_stack	*new_stack(t_stack_name name)
{
	t_stack	*ptr;

	ptr = malloc(sizeof(t_stack));
	if (!ptr)
		return (ptr);
	ptr->head = 0;
	ptr->tail = 0;
	ptr->size = 0;
	ptr->name = name;
	return (ptr);
}

void	clear_stack(t_stack **stack)
{
	t_node	*head;
	t_node	*tail;
	t_node	*next;

	if (stack && *stack)
	{
		head = (*stack)->head;
		tail = (*stack)->tail;
		while (head)
		{
			next = head->next;
			free(head);
			if (head == tail)
				break ;
			head = next;
		}
		free(*stack);
		*stack = 0;
	}
}

t_stack	*clone_stack(t_stack *origin)
{
	t_stack			*stack;
	unsigned long	i;
	t_node			*el;
	t_node			*copy;

	i = 0;
	el = 0;
	stack = new_stack(origin->name);
	if (!stack)
		return (stack);
	el = origin->head;
	while (i < origin->size)
	{
		copy = clone_unlinked_node(el);
		if (!copy)
			return (stack);
		stack_add_back(stack, copy);
		el = el->next;
		i++;
	}
	return (stack);
}
