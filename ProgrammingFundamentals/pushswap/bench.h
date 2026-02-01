/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 15:47:25 by maziza            #+#    #+#             */
/*   Updated: 2025/12/10 15:48:55 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BENCH_H
# define BENCH_H
# include "pushswap.h"

void	ft_bench(t_input input, t_output *out, float float_disorder);
int		*ft_array_values(t_stack *mainstack);
float	compute_disorder(int *a, unsigned int len);
int		displayable_disorder(float disorder);
char	*di(int disorder);

typedef struct s_nb_ops
{
	int	sa;
	int	sb;
	int	ss;
	int	pa;
	int	pb;
	int	ra;
	int	rb;
	int	rr;
	int	rra;
	int	rrb;
	int	rrr;
}		t_nb_ops;

#endif
