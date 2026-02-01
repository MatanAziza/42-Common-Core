/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 15:39:05 by maziza            #+#    #+#             */
/*   Updated: 2025/12/14 19:14:41 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "bench.h"
#include "ft_output.h"
#include "ft_printf.h"
#include "pushswap.h"
#include <stdlib.h>
#include <unistd.h>

int	*ft_array_values(t_stack *mainstack)
{
	int				*a;
	unsigned long	i;

	i = 0;
	a = malloc(sizeof(int) * (mainstack->size));
	while (i < mainstack->size)
	{
		a[i++] = mainstack->head->value;
		mainstack->head = mainstack->head->next;
	}
	return (a);
}

t_nb_ops	*ft_init_count(void)
{
	t_nb_ops	*count_ops;

	count_ops = malloc(sizeof(t_nb_ops));
	if (count_ops)
	{
		count_ops->pa = 0;
		count_ops->pb = 0;
		count_ops->ra = 0;
		count_ops->rb = 0;
		count_ops->rr = 0;
		count_ops->rra = 0;
		count_ops->rrb = 0;
		count_ops->rrr = 0;
		count_ops->sa = 0;
		count_ops->sb = 0;
		count_ops->ss = 0;
	}
	return (count_ops);
}

void	count(t_operation_list *list, t_nb_ops *count_ops)
{
	if (list->op == OP_PA)
		count_ops->pa++;
	else if (list->op == OP_PB)
		count_ops->pb++;
	else if (list->op == OP_RA)
		count_ops->ra++;
	else if (list->op == OP_RB)
		count_ops->rb++;
	else if (list->op == OP_RR)
		count_ops->rr++;
	else if (list->op == OP_RRA)
		count_ops->rra++;
	else if (list->op == OP_RRB)
		count_ops->rrb++;
	else if (list->op == OP_RRR)
		count_ops->rrr++;
	else if (list->op == OP_SA)
		count_ops->sa++;
	else if (list->op == OP_SB)
		count_ops->sb++;
	else if (list->op == OP_SS)
		count_ops->ss++;
}

t_nb_ops	*ft_parse_ops(t_output *out)
{
	t_operation_list	*list;
	t_nb_ops			*count_ops;

	count_ops = ft_init_count();
	list = out->ops;
	while (list && count_ops)
	{
		count(list, count_ops);
		list = list->next;
	}
	return (count_ops);
}

void	ft_bench(t_input input, t_output *out, float float_disorder)
{
	int			disorder;
	t_nb_ops	*count_ops;

	disorder = displayable_disorder(float_disorder);
	ft_printf(2, "[bench] disorder: %d.%d%%\n", disorder / 100, disorder % 100);
	if (input.adaptive)
		ft_printf(2, "[bench] strategy: Adaptive / %s\n", di(disorder));
	else if (input.medium)
		ft_printf(2, "[bench] strategy: Medium / O(n√n)\n");
	else if (input.simple)
		ft_printf(2, "[bench] strategy: Simple / O(n²)\n");
	else
		ft_printf(2, "[bench] strategy: Complex / O(nlog(n))\n");
	ft_printf(2, "[bench] total_ops: %d\n", output_len(out));
	count_ops = ft_parse_ops(out);
	if (!count_ops)
		return ;
	ft_printf(2, "[bench] sa: %d sb: %d ss: %d pa: %d pb: %d\n", count_ops->sa,
		count_ops->sb, count_ops->ss, count_ops->pa, count_ops->pb);
	ft_printf(2, "[bench] ra: %d rb: %d rr: %d rra: %d rrb: %d rrr:%d\n",
		count_ops->ra, count_ops->rb, count_ops->rr, count_ops->rra,
		count_ops->rrb, count_ops->rrr);
}
