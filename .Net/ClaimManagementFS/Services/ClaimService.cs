using ClaimsManagement.Data;
using ClaimsManagement.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ClaimsManagement.Services
{
    public class ClaimService : IClaimService
    {
        private readonly ApplicationDbContext _context;

        public ClaimService(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Claim>> GetAllClaimsAsync()
        {
            return await _context.Claims.ToListAsync();
        }

        public async Task<Claim> GetClaimByIdAsync(int id)
        {
            return await _context.Claims.FindAsync(id);
        }

        public async Task<Claim> CreateClaimAsync(Claim claim)
        {
            _context.Claims.Add(claim);
            await _context.SaveChangesAsync();
            return claim;
        }

        public async Task<Claim> UpdateClaimAsync(int id, Claim updatedClaim)
        {
            var claim = await _context.Claims.FindAsync(id);
            if (claim == null) return null;

            claim.Title = updatedClaim.Title;
            claim.Description = updatedClaim.Description;
            claim.DateSubmitted = updatedClaim.DateSubmitted;
            claim.TypeOfReclamation = updatedClaim.TypeOfReclamation;
            claim.Status = updatedClaim.Status;

            await _context.SaveChangesAsync();
            return claim;
        }

        public async Task DeleteClaimAsync(int id)
        {
            var claim = await _context.Claims.FindAsync(id);
            if (claim != null)
            {
                _context.Claims.Remove(claim);
                await _context.SaveChangesAsync();
            }
        }
    }
}
