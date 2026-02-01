/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: maziza <matan.aziza@learner.42.tech>       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/12 13:35:07 by maziza            #+#    #+#             */
/*   Updated: 2025/11/12 13:35:12 by maziza           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putchar(int fd, char c)
{
	return (write(fd, &c, 1));
}

int	ft_putnbr_base(int fd, long int nb, const char *base, int sign)
{
	char		c;
	long int	nbr;
	int			len;
	int			count;

	count = 0;
	if (sign == 0)
		nbr = (unsigned)nb;
	else
		nbr = nb;
	if (nbr < 0)
	{
		nbr = -nbr;
		count += ft_putchar(fd, '-');
		count += ft_putnbr_base(fd, nbr, base, sign);
		return (count);
	}
	len = ft_strlen((char *)base);
	if (nbr / len != 0)
		count += ft_putnbr_base(fd, nbr / len, base, sign);
	c = base[nbr % len];
	count += ft_putchar(fd, c);
	return (count);
}

int	ft_putstr(int fd, char *s)
{
	int	i;

	i = 0;
	if (!s)
		return (write(fd, "(null)", 6));
	while (s[i])
	{
		ft_putchar(fd, s[i]);
		i++;
	}
	return (i);
}

int	ft_putnbr_address(int fd, unsigned long nbr, const char *base)
{
	char	c;
	int		count;

	count = 0;
	if (nbr / 16 != 0)
		count += ft_putnbr_address(fd, nbr / 16, base);
	c = base[nbr % 16];
	count += ft_putchar(fd, c);
	return (count);
}

int	ft_print_address(int fd, unsigned long address, const char *base)
{
	int	count;

	count = 0;
	if (address == 0)
		return (count + write(fd, "(nil)", 5));
	count += write(fd, "0x", 2);
	return (count + ft_putnbr_address(fd, address, base));
}
