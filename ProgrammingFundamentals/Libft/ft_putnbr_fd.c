/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <maziza@student.42.fr>              +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 11:04:16 by maziza            #+#    #+#             */
/*   Updated: 2025/11/13 09:27:12 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putnbr_fd(int nb, int fd)
{
	char	c;

	if (nb == -2147483648)
	{
		write(fd, "-2147483648", 11);
		return ;
	}
	if (nb < 0)
	{
		nb = -nb;
		write(fd, "-", 1);
		ft_putnbr_fd(nb, fd);
		return ;
	}
	if (nb / 10 != 0)
		ft_putnbr_fd(nb / 10, fd);
	c = nb % 10 + '0';
	ft_putchar_fd(c, fd);
	return ;
}
