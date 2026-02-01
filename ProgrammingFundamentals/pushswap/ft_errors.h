/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_errors.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/28 13:45:17 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/14 19:26:10 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_ERRORS_H
# define FT_ERRORS_H

# include "ft_stack.h"

typedef struct s_conversion_result
{
	int		err;
	long	value;
}			t_conversion_result;

typedef int	t_error;
#endif
