/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bubble_sort.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/02 15:39:55 by maziza            #+#    #+#             */
/*   Updated: 2025/12/02 17:04:09 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_stack.h"

void	bubble_sort(t_stack *a, t_stack *b, t_output *out)
{
	unsigned int	i;

	i = 0;
	while (a->size)
	{
		if (i == a->size)
		{
			push(a, b, out);
			i = 0;
		}
		if (a->head->value <= a->head->next->value)
			swap(a, out);
		rotate(a, out);
		i++;
	}
	while (b->size)
		push(b, a, out);
}
