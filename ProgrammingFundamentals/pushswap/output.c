/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   output.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/02 15:22:02 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:22:47 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// These methods will not set next and prev if there were no
// elements on the stack.
// #include "ft_errors.h"
#include "ft_output.h"
#include <stdlib.h>

t_operation_list	*new_operation(t_operation op)
{
	t_operation_list	*new;

	new = malloc(sizeof(t_operation_list));
	if (new)
	{
		new->op = op;
		new->next = 0;
	}
	return (new);
}

t_output	*new_output(void)
{
	t_output	*new;

	new = malloc(sizeof(t_output));
	if (new)
	{
		new->count = 0;
		new->ops = 0;
	}
	return (new);
}

// Do we want this to return a type of error on alloc fail ?
void	output_add_back(t_output *output, t_operation op)
{
	t_operation_list	*list;

	if (output)
	{
		if (output->ops)
		{
			list = output->ops;
			while (list->next)
			{
				list = list->next;
			}
			list->next = new_operation(op);
		}
		else
			output->ops = new_operation(op);
		(output->count)++;
	}
}

int	ft_lstsize(t_operation_list *lst)
{
	int	cont;

	cont = 0;
	while (lst != NULL)
	{
		cont++;
		lst = lst->next;
	}
	return (cont);
}

int	output_len(t_output *output)
{
	t_operation_list	*list;
	int					count;

	count = 0;
	if (output && output->ops)
	{
		list = output->ops;
		count = ft_lstsize(list);
	}
	return (count);
}
