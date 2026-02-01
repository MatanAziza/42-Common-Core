/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pushswap.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 16:28:19 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/01 15:43:49 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSHSWAP_H
# define PUSHSWAP_H
# include "ft_errors.h"
# include "ft_stack.h"

typedef struct s_input
{
	int	adaptive;
	int	simple;
	int	complex;
	int	medium;
	int	bench;

	int	found;
}		t_input;

t_input	new_input_marker(void);
t_error	treat_input(int argc, char **argv, t_stack *head, t_input *input);
#endif
