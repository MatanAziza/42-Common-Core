/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_output.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jenicola <jean.nicolas-de-lamballerie@lea  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/01 15:24:24 by jenicola          #+#    #+#             */
/*   Updated: 2025/12/05 18:21:30 by jenicola         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_OUTPUT_H
# define FT_OUTPUT_H

typedef enum e_operation
{
	OP_SA,
	OP_SB,
	OP_SS,
	OP_PA,
	OP_PB,
	OP_RA,
	OP_RB,
	OP_RR,
	OP_RRA,
	OP_RRB,
	OP_RRR,
}							t_operation;

typedef struct s_operation_list
{
	t_operation				op;
	struct s_operation_list	*next;
}							t_operation_list;

typedef struct s_output
{
	t_operation_list		*ops;
	int						count;
}							t_output;

t_output					*new_output(void);
void						clear_output(t_output **out);
void						output_add_back(t_output *output, t_operation op);
int							output_len(t_output *output);
const char					*op_str(t_operation op);
void						optimize_cancel(t_output *out);
void						optimize_combine(t_output *out);
void						optimize_ops(t_output *out);
#endif
