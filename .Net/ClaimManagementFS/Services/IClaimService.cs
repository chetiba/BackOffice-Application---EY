using ClaimsManagement.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ClaimsManagement.Services
{
    public interface IClaimService
    {
        Task<IEnumerable<Claim>> GetAllClaimsAsync();
        Task<Claim> GetClaimByIdAsync(int id);
        Task<Claim> CreateClaimAsync(Claim claim);
        Task<Claim> UpdateClaimAsync(int id, Claim claim);
        Task DeleteClaimAsync(int id);
    }
}
