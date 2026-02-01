/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   minmax.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/04 19:42:41 by maziza            #+#    #+#             */
/*   Updated: 2025/12/05 18:34:43 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_algorithms.h"
#include "ft_stack.h"

void	minmax(t_stack *a, t_stack *b, t_output *out)
{
	unsigned long	index_nbr;
	t_position		order;

	index_nbr = 0;
	while (a->size)
	{
		order = order_rotation(a, index_nbr);
		while (a->head->idx != index_nbr)
		{
			if (order == R)
				rotate(a, out);
			else
				reverse_rotate(a, out);
		}
		push(a, b, out);
		index_nbr++;
	}
	while (b->size)
		push(b, a, out);
}
