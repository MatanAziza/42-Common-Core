/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   optimization_output_cancel.c                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/19 17:50:22 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/19 18:04:31 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_output.h"
#include <stdlib.h>

// helper: cancel inverses / duplicates in the output list.
static int	ops_cancel(t_operation a, t_operation b)
{
	if ((a == OP_RA && b == OP_RRA) || (a == OP_RRA && b == OP_RA))
		return (1);
	if ((a == OP_RB && b == OP_RRB) || (a == OP_RRB && b == OP_RB))
		return (1);
	if ((a == OP_PA && b == OP_PB) || (a == OP_PB && b == OP_PA))
		return (1);
	if ((a == OP_SA && b == OP_SA) || (a == OP_SB && b == OP_SB))
		return (1);
	return (0);
}

static void	remove_elements(t_operation_list *curr, t_operation_list *next,
		t_output *out)
{
	free(curr);
	free(next);
	out->count -= 2;
}

static int	cancel(t_operation_list **next, t_operation_list **prev,
		t_operation_list **curr, t_output *out)
{
	*next = (*curr)->next;
	(*prev)->next = (*next)->next;
	remove_elements(*curr, *next, out);
	*curr = (*prev)->next;
	return (1);
}

static int	cancel_pass(t_output *out)
{
	t_operation_list	dummy;
	t_operation_list	*prev;
	t_operation_list	*curr;
	t_operation_list	*next;
	int					count;

	count = 0;
	dummy.next = out->ops;
	prev = &dummy;
	curr = out->ops;
	while (curr && curr->next)
	{
		if (ops_cancel(curr->op, curr->next->op))
			count += cancel(&next, &prev, &curr, out);
		else
		{
			prev = curr;
			curr = curr->next;
		}
	}
	out->ops = dummy.next;
	return (count);
}

// pass 1: remove canceling ops
void	optimize_cancel(t_output *out)
{
	while (cancel_pass(out))
		;
}
