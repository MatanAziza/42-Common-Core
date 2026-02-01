/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/17 11:04:54 by maziza            #+#    #+#             */
/*   Updated: 2025/11/17 11:06:43 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H
# include <stdlib.h>
# include <unistd.h>
# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif
# ifndef NEW_LINE
#  define NEW_LINE '\n'
# endif

typedef struct s_store
{
	char	str[BUFFER_SIZE + 1];
	int		len;
}			t_store;

typedef struct s_join
{
	char	*s1;
	char	*s2;
	int		b1;
	int		b2;
}			t_join;

void		*ft_frees(t_join *join);
int			ft_strcpy(char *dest, char *src);
char		*ft_strdup(char *s);
int			ft_strchr(const char *s, int c);
char		*ft_strjoin(t_join *str);
char		*ft_substr(char *s, unsigned int start, size_t len);
char		*get_next_line(int fd);
#endif
