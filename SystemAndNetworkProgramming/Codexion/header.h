/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 17:34:10 by maziza            #+#    #+#             */
/*   Updated: 2026/06/25 14:22:42 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

# include <pthread.h>
# include "structs.h"
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <unistd.h>

int		filler(char **args, t_data *p_data);
void	*print_name(void *arg);
void	*thread_function(void *arg);
void	fill_dongle(t_dongle *dongle, int cd);
t_coder	fill_coder(t_data *data, int id);
int		check_arg_int(char *arg);
int		fifo(t_coder coder);
int		edf(t_coder coder);
void	swap(int *a, int *b, int cond);
int		free_all(pthread_t **threads, t_data *data);
int		free_values(int *values);

#endif
