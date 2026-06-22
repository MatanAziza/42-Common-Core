/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 17:34:10 by maziza            #+#    #+#             */
/*   Updated: 2026/06/22 17:30:43 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

# include <pthread.h>
# include <stdlib.h>
# include <stdio.h>
# include <unistd.h>
# include <string.h>
# include "structs.h"

void	filler(char **args, t_data	*p_data);
int		parse_check(char **argv);
void	fill_dongle(t_dongle *dongle, int cd);
void	free_data(t_data data);
int		free_atoied(int	*atoied);
void	add_to_queues(t_coder *coder);
int		fifo(t_queue *queue);
int		edf(t_queue *queue);

#endif
