/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/18 13:38:21 by maziza            #+#    #+#             */
/*   Updated: 2025/11/20 10:36:33 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

void	*ft_frees(t_join *join)
{
	if (join)
	{
		if (join->s1)
			free(join->s1);
		if (join->s2)
			free(join->s2);
		free(join);
	}
	return (NULL);
}

void	ft_fill_s2(int fd, t_join **join, t_store *store)
{
	if (store->str[0])
	{
		(*join)->s2 = ft_strdup(store->str);
		(*join)->b2 = store->len;
		store->str[0] = '\0';
		store->len = 0;
	}
	else
	{
		(*join)->s2 = malloc(sizeof(char) * (BUFFER_SIZE + 1));
		if (!(*join)->s2)
			return ;
		(*join)->b2 = read(fd, (*join)->s2, BUFFER_SIZE);
		if ((*join)->b2 >= 0)
			(*join)->s2[(*join)->b2] = '\0';
	}
}

char	*ft_gnl1(int fd, t_join **join, t_store *store)
{
	char	*ret;
	int		ni;

	ni = -1;
	while (ni == -1)
	{
		ft_fill_s2(fd, join, store);
		if ((*join)->b2 <= 0)
			return (ft_strdup((*join)->s1));
		if (!(*join)->s2[0])
			return ((*join)->s2);
		(*join)->s1 = ft_strjoin(*join);
		(*join)->s2 = NULL;
		(*join)->b1 += (*join)->b2;
		ni = ft_strchr((*join)->s1, NEW_LINE);
		if (ni != -1)
		{
			store->len = ft_strcpy(store->str, (*join)->s1 + ni + 1);
			ret = ft_substr((*join)->s1, 0, ni + 1);
			(*join)->s1 = NULL;
		}
	}
	return (ret);
}

char	*get_next_line(int fd)
{
	static t_store	store = {{0}, 0};
	t_join			*join;
	char			*ret;

	join = malloc(sizeof(struct s_join));
	if (!join)
		return (ft_frees(join));
	join->s1 = NULL;
	join->b1 = 0;
	join->s2 = NULL;
	join->b2 = 0;
	ret = ft_gnl1(fd, &join, &store);
	ft_frees(join);
	return (ret);
}

/*int	main(void)
{
	int		fd;
	char	*line;
	int		i;

	i = 0;
	fd = open("get_next_line.c", O_RDONLY);
	while (i < 20)
	{
		line = get_next_line(fd);
		printf("line : %s", line);
		free(line);
		i++;
	}
	return (0);
}*/
