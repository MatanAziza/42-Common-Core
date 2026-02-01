/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   node.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 13:42:07 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:15:19 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"
#include <stdlib.h>

t_node	*new_stack_member(long value)
{
	t_node	*node;

	node = malloc(sizeof(t_node));
	if (!node)
		return (0);
	node->value = value;
	node->idx = 0;
	node->next = 0;
	node->previous = 0;
	return (node);
}

t_node	*clone_unlinked_node(t_node *source)
{
	t_node	*node;

	node = malloc(sizeof(t_node));
	if (!node)
		return (0);
	node->idx = source->idx;
	node->value = source->value;
	node->next = 0;
	node->previous = 0;
	return (node);
}
