using Microsoft.EntityFrameworkCore;
using ClaimsManagement.Models;

namespace ClaimsManagement.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        public DbSet<Claim> Claims { get; set; }
    }
}
