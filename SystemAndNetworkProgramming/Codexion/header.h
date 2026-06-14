/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/12 17:34:10 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 18:30:05 by maziza           ###   ########.fr       */
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

int		free_atoied(int	*atoied);
void	parser(char **args, t_data	*p_data);
int		parse_check(char **argv);
void	fill_dongle(t_dongle *dongle, int id, int cd);

#endif
