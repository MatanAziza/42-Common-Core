/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   structs.h                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/11 20:39:06 by maziza            #+#    #+#             */
/*   Updated: 2026/06/12 18:30:01 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef STRUCTS_H
# define STRUCTS_H

# include <bits/pthreadtypes.h>
enum					CoderState
{
	COMPILING,
	DEBUGGING,
	REFACTORING,
	WAITING
};

typedef struct s_coder
{
	int					id;
	enum CoderState		state;
	int					burnout_time;
	int					compile_time;
	int					debug_time;
	int					refactor_time;
	int					nb_compile;
	int					nb_threads;
	int					max_compile;
	struct s_dongle		*dongles;
}						t_coder;

typedef struct s_dongle
{
	int					available;
	int					cooldown;
	int					timer;
	pthread_mutex_t		mutexDongle;
	pthread_cond_t		condDongle;
}						t_dongle;

typedef struct s_data
{
	struct s_coder		*coders;
	struct s_dongle		*dongles;
}						t_data;

#endif
