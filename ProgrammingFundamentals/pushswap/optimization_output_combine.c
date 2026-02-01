/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   optimization_output.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 18:17:22 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/19 17:56:29 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_output.h"
#include <stdlib.h>

// helper: combine patterns in the output list.
int	ops_combine(t_operation a, t_operation b, t_operation *out)
{
	if ((a == OP_RA && b == OP_RB) || (a == OP_RB && b == OP_RA))
	{
		*out = OP_RR;
		return (1);
	}
	if ((a == OP_RRA && b == OP_RRB) || (a == OP_RRB && b == OP_RRA))
	{
		*out = OP_RRR;
		return (1);
	}
	if ((a == OP_SA && b == OP_SB) || (a == OP_SB && b == OP_SA))
	{
		*out = OP_SS;
		return (1);
	}
	return (0);
}

// pass 2: combine patterns
void	optimize_combine(t_output *out)
{
	t_operation_list	*curr;
	t_operation			newop;
	t_operation_list	*tmp;

	curr = out->ops;
	while (curr && curr->next)
	{
		newop = -1;
		if (ops_combine(curr->op, curr->next->op, &newop))
		{
			curr->op = newop;
			tmp = curr->next;
			curr->next = tmp->next;
			free(tmp);
			out->count--;
		}
		else
			curr = curr->next;
	}
}
